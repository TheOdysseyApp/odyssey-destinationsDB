# create DB client and other customized helper functions

import os
import boto3
from dotenv import load_dotenv

load_dotenv()

def create_client(service_name: str, region_name: str):
    """
    DB client creator

    Returns:
        DB service client instance
    """
    ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
    SCERET_ACCESS_KEY = os.getenv("SCERET_ACCESS_KEY")
    client = boto3.client(
        service_name=service_name,
        region_name=region_name,
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SCERET_ACCESS_KEY
    )
    return client
