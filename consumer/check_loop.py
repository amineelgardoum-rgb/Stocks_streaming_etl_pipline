import time
from kafka import errors
from display_logging import logging
def wait_for_kafka(broker,port,retires=10,delay=5):
    from kafka import KafkaAdminClient
    for i  in range(retires):
        try:
            admin=KafkaAdminClient(bootstrap_servers=f'{broker}:{port}')
            admin.list_topics()
            logging.info('Kafka is ready.')
            admin.close()
            return 
        except errors.NoBrokersAvailable:
            logging.info(f"Waiting for Kafka {i+1}/{retires}.")
            time.sleep(delay)
    raise RuntimeError("Kafka is not available.")