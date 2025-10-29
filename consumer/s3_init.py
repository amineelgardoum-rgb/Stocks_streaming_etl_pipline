import boto3
from botocore.exceptions import ClientError
from display_logging import logging
def create_s3(endpoint_url,aws_access_key_id,aws_secret_access_key,bucket_name):
    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    bucket_name = bucket_name
    try:
        s3.head_bucket(Bucket=bucket_name)
        logging.info(f"The bucket {bucket_name} already exists.")
    except ClientError:
        s3.create_bucket(Bucket=bucket_name)
        logging.info(f"Created the {bucket_name}.")
        
        
    return s3