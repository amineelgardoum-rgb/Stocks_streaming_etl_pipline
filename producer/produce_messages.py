import time
from display_logging import logging


def produce_messages(
    SYMBOLS, fetch_quotes, send_messages, BASE_URL, api_key, qoute_topic
):
    logging.info(".........Starting the data pipeline.........")
    while True:
        for symbol in SYMBOLS:
            quote = fetch_quotes(symbol, BASE_URL, api_key)
            if quote:
                logging.info(f"Producing:{quote}")
                send_messages(value=quote, topic=qoute_topic)
        time.sleep(6)
