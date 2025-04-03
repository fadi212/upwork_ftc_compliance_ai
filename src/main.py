import os
from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field
import uvicorn
from src.data_processing.file_processing import process_text, count_tokens
from src.data_processing.router_setup import load_category_from_s3, init_router
from src.config.config import logger, S3Config
import boto3
from contextlib import contextmanager
from threading import Lock

app = FastAPI()

s3_client = boto3.client(
    's3',
    aws_access_key_id=S3Config.ACCESS_KEY,
    aws_secret_access_key=S3Config.SECRET_ACCESS_KEY,
    region_name=S3Config.REGION
)

API_KEY = os.getenv('API_KEY')

# Cache to store the router layers
router_cache = {}
cache_lock = Lock()


class TextProcessRequest(BaseModel):
    text: str
    category: str
    severity: int = Field(default=3, description="Severity level of the tagged sentence")
    refresh: bool = Field(default=False, description="Flag to refresh the router layer for the category")


def verify_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        logger.error("Invalid API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )


@contextmanager
def get_router_layer(category, refresh):
    with cache_lock:
        if category in router_cache and not refresh:
            logger.info(f"Using cached router layer for category: {category}")
            yield router_cache[category]
        else:
            if refresh:
                logger.info(f"Refreshing router layer for category: {category}")
            else:
                logger.info(f"Loading category {category} from S3 bucket")

            category_data = load_category_from_s3(s3_client, S3Config.BUCKET_NAME, category)
            if not category_data:
                logger.error(f"Category {category} not found in S3 bucket")
                raise HTTPException(status_code=200, detail="Category not found")

            router_layer = init_router(category, category_data)
            router_cache[category] = router_layer
            yield router_layer


@app.post("/process_text")
async def process_text_api(request_body: TextProcessRequest, request: Request):
    verify_api_key(request)
    category = request_body.category
    severity = request_body.severity  # Get the severity value from the request
    refresh = request_body.refresh  # Get the refresh flag from the request
    logger.info(
        f"Received request to process text for category: {category} with severity: {severity} and refresh: {refresh}")

    with get_router_layer(category, refresh) as router_layer:
        logger.info(f"Router layer initialized for category: {category}")

        num_tokens = count_tokens(text=request_body.text)
        logger.debug(f"Number of tokens in input text: {num_tokens}")

        tagged_sentences = process_text(router_layer, request_body.text)
        logger.info(f"Tagging completed. Found {len(tagged_sentences)} tagged sentences.")

        # Set the severity for each tagged sentence
        for sentence_data in tagged_sentences:
            sentence_data["severity"] = severity

        response = {
            "sentences": tagged_sentences or [],
            "usage": {
                "prompt_tokens": num_tokens,
                "completion_tokens": 0
            }
        }

    logger.debug(f"Response ready to be sent: {response}")
    return response


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)
