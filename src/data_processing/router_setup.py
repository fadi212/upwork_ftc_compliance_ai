import pandas as pd
from semantic_router import Route, RouteLayer
from semantic_router.encoders import OpenAIEncoder
from semantic_router.index.local import LocalIndex
from src.config.config import logger
import io


def load_category_from_s3(s3_client, bucket_name, category_name):
    file_key = f'categories/{category_name}.csv'
    logger.info(f"Loading category {category_name} from S3 bucket {bucket_name}")
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        logger.info(f"Successfully loaded category {category_name} from S3")
        file_content = response['Body'].read().decode('utf-8', errors='replace')
        df = pd.read_csv(io.StringIO(file_content), quotechar='"', escapechar="\\", on_bad_lines='warn')

        # Extract categories and texts
        categories = {}
        for index, row in df.iterrows():
            category = row['category']
            text = row['text']
            if category not in categories:
                categories[category] = []
            categories[category].append(text)

        return categories
    except Exception as e:
        logger.error(f"Error loading category {category_name} from S3: {str(e)}")
        return None


def init_router(category, categories, index='local'):
    logger.info(f"Initializing router instance for category {category}.")

    routes = [Route(name=category_name, utterances=texts) for category_name, texts in categories.items()]
    encoder = OpenAIEncoder(name="text-embedding-ada-002", score_threshold=0.83)

    index_instance = LocalIndex()

    router_instance = RouteLayer(encoder=encoder, routes=routes, index=index_instance)
    logger.info(f"Router instance initialized for category {category}.")

    return router_instance
