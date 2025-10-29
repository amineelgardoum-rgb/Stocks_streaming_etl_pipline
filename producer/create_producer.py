# from math import prod
from kafka import KafkaProducer
import json
from display_logging import logging


def create_producer(broker, port, topics=None):
    producer = KafkaProducer(
        bootstrap_servers=[f"{broker}:{port}"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    def send_messages(value, topic=None):
        if topic is None:
            if not topics:
                raise ValueError("No Topic specified and no default topics set !")
            for t in topics:
                logging.info(f"sending data to {t}.")
                producer.send(t, value=value)
        else:
            logging.info(f"sending data to topic:{topic}.")
            producer.send(topic, value=value)

    logging.info("Producer Created Successfully.")

    return producer, send_messages
