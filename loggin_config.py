import logging
import sys
import os


def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO")

    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.handlers = []  # Remove default handlers
    logger.addHandler(handler)
