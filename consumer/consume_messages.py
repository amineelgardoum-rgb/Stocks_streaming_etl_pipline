import json
import time
from display_logging import logging
def consume_messages(consumer,s3,bucket_name):
    logging.info("###########################################################################################")
    logging.info("#################################### Saving Stage in MINIO ################################")
    logging.info("###########################################################################################")
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
        logging.info(f"Saved record for {symbol}= s3://{bucket_name}/{key}...")
