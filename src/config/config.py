import os
from openai import OpenAI
import logging


def setup_logger():
    logger = logging.getLogger("semantic_router")
    logger.setLevel(logging.DEBUG)  # Set the logger to capture all levels

    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)

    f_handler = logging.FileHandler('semantic_router.log')
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


logger = setup_logger()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class S3Config:
    ACCESS_KEY = ''
    SECRET_ACCESS_KEY = ''
    REGION = ''
    BUCKET_NAME = ''
