from math import log
import requests
import time
from display_logging import logging


def fetch_quotes(symbol, BASE_URL, api_key):
    url = f"{BASE_URL}?symbol={symbol}&token={api_key}"
    try:
        logging.info("Starting the fetch job from the API .........")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data["symbol"] = symbol
        data["fetched_time"] = int(time.time())
        return data
    except Exception as e:
        print(f"There is a problem :{e}!,with {symbol}.")
        return None
