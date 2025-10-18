# ------ consumer logic ------ #
import boto3
import json
from kafka import KafkaConsumer
import time
from botocore.exceptions import ClientError
# init the s3 client
s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id="admin",
    aws_secret_access_key="password123",
)
bucket_name = "bronze-transactions"
try:
    s3.head_bucket(Bucket=bucket_name)
    print(f"The bucket {bucket_name} already exists.")
except ClientError:
    s3.create_bucket(Bucket=bucket_name)
    print(f"Created the {bucket_name}.")
    
# s3.create_bucket(Bucket=bucket_name)
# define the consumer
consumer = KafkaConsumer(
    "stock_qoutes",
    bootstrap_servers=["kafka:9092"],
    enable_auto_commit=True,
    group_id="bronze-consumer",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)
print("Customer streaming and saving to MINIO.........")
for message in consumer:
    record = message.value
    symbol = record.get("symbol")
    ts = record.get("fetched_time", int(time.time()))  # time served
    key = f"{symbol}/{ts}.json"  # to format the objects in minio bucket
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(record),
        ContentType="application/json",
    )
    print(f"Saved record for {symbol}= s3://{bucket_name}/{key}")
