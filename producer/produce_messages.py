import time
from display_logging import logging
from metrics_mon import start_http_server,record_messages_producer


def produce_messages(
    SYMBOLS, fetch_quotes, send_messages, BASE_URL, api_key, qoute_topic
):
    start_time=time.time()
    logging.info(".........Starting the data pipeline.........")
    while True:
        for symbol in SYMBOLS:
            quote = fetch_quotes(symbol, BASE_URL, api_key)
            if quote:
                logging.info(f"Producing:{quote}")
                send_messages(value=quote, topic=qoute_topic)
                record_messages_producer(start_time)
        time.sleep(6)
