import threading
from display_logging import logging


def start_thread(task):
    logging.info("Starting the thread to track the heartbeat of the producer.")
    threading.Thread(target=task, daemon=True).start()
