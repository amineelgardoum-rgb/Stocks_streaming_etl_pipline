import time
from create_producer import create_producer

producer, send_messages = create_producer("kafka", 9092)
heartbeat_topic = "heartbeat_topic"


def heartbeat_check():
    while True:
        msg = {
            "service": "stock_producer",
            "status": "alive",
            "timestamp": int(time.time()),
        }
        send_messages(value=msg, topic=heartbeat_topic)
        print(f"Heartbeat Sent: {msg}.")
        time.sleep(10)
