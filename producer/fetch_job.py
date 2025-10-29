import requests
import time


def fetch_quotes(symbol, BASE_URL, api_key):
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
