import logging
import os

def get_logger(log_file_path, log_level=logging.INFO):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    custom_logger = logging.getLogger(log_file_path)
    custom_logger.setLevel(log_level)

    if not custom_logger.handlers:
        handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        custom_logger.addHandler(handler)

    return custom_logger
