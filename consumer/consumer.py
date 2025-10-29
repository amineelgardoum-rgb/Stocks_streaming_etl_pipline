# ------ consumer logic ------ #
from consume_messages import consume_messages
from display_logging import logging
# import os
from create_consumer import create_consumer
from s3_init import create_s3
from check_loop import wait_for_kafka

bucket_name = "bronze-transactions"
endpoint_url = "http://minio:9000"
MINIO_ROOT_USER = "admin"
MINIO_ROOT_PASSWORD = "password123"
s3 = create_s3(endpoint_url, MINIO_ROOT_USER, MINIO_ROOT_PASSWORD, bucket_name)
topic = "stock_qoutes"
broker = "kafka"
port = 9092
enable_auto_commit = True
group_id = "bronze-consumer"
auto_offset_reset = "earliest"
wait_for_kafka(broker=broker, port=port)
consumer = create_consumer(topic, broker, port, True, group_id, auto_offset_reset)
logging.info("################################################################################################")
logging.info(f"Customer streaming and saving to MINIO.........,under the topic: {topic}..., and the bucket: {bucket_name}...")
logging.info("###########################################################################################")
consume_messages(consumer, s3, bucket_name)
