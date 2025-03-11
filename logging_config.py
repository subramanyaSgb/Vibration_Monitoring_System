import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

def setup_logger():
    # Create a logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a TimedRotatingFileHandler
    log_filename = f"logs/app_log_{datetime.now().strftime('%Y-%m-%d')}.log"
    handler = TimedRotatingFileHandler(
        log_filename,
        # when="m",
        when="midnight",
        interval=1,
        backupCount=1,  # Keep 0 backup files (delete old logs)
    )

    # Create a formatter that includes the filename
    formatter = logging.Formatter('%(asctime)s | %(filename)s | %(threadName)s | [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger

# Use this logger in both server.py and main.py
logger = setup_logger()

# Example usage in server.py:
# logger.info("This is a log message from server.py")

# Example usage in main.py:
# logger.info("This is a log message from main.py")