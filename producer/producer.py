# ----- producer of kafka to make the streaming logic ------- #
from display_logging import logging
from create_producer import create_producer
from fetch_job import fetch_quotes
import os
from heartbeat import heartbeat_check
import threading
from dotenv import load_dotenv
from produce_messages import produce_messages

load_dotenv()  # just to load the env file
api_key = os.getenv("api_key")
if not api_key:
    raise RuntimeError("the api_key is not set ")

heartbeat_topic = "heartbeat_topic"
qoute_topic = "stock_qoutes"
BASE_URL = "https://finnhub.io/api/v1/quote"
SYMBOLS = ["AAPL", "TSLA", "GOOGL", "AMZN"]  # this are the companies to monitor
# init of producer
producer, send_messages = create_producer(
    "kafka", 9092, topics=[qoute_topic, heartbeat_topic]
)
threading.Thread(target=heartbeat_check, daemon=True).start()

produce_messages(SYMBOLS, fetch_quotes, send_messages, BASE_URL, api_key, qoute_topic)
