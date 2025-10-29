from kafka import KafkaConsumer
import json
from display_logging import logging
def create_consumer(topic,broker,port,enable_auto_commit,group_id,auto_offset_reset):
    consumer = KafkaConsumer(
    topic,
    bootstrap_servers=[f"{broker}:{port}"],
    enable_auto_commit=enable_auto_commit,
    group_id=group_id,
    auto_offset_reset=auto_offset_reset,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)
    logging.info("###########################################################################################")
    logging.info("################################## Consumer Created Successfully.... ######################")
    logging.info("###########################################################################################")
    return consumer
