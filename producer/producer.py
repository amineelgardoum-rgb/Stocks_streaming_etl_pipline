# ----- producer of kafka to make the streaming logic ------- #
import time
from kafka import KafkaProducer
import requests
import json
# import logging
import os
from dotenv import load_dotenv

load_dotenv()  # just to load the env file
api_key = os.getenv("api_key")
if not api_key:
    raise RuntimeError("the api_key is not set ")

BASE_URL = "https://finnhub.io/api/v1/quote"
SYMBOLS = ["AAPL","TSLA", "GOOGL", "AMZN"]  # this are the companies to monitor
# init of producer
producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    max_request_size=2 * 1024 * 1024,
)


def fetch_quotes(symbol):
    url = f"{BASE_URL}?symbol={symbol}&token={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data["symbol"] = symbol
        data["fetched_time"] = int(time.time())
        return data
    except Exception as e:
        print(f"There is a problem :{e}!,with {symbol}.")
        return None


while True:
    for symbol in SYMBOLS:
        quote = fetch_quotes(symbol)
        if quote:
            print(f"Producing:{quote}")
            producer.send("stock_qoutes", value=quote)
    time.sleep(6)
