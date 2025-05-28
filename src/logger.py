import os
import logging

def get_logger(name: str) -> logging.Logger:
    os.makedirs('logs', exist_ok=True)

    logger = logging.getLogger(name)

    # Prevent duplicate handlers if get_logger is called multiple times
    if not logger.handlers:
        file_handler = logging.FileHandler(f'logs/{name}.log')
        file_handler.setLevel(logging.WARNING)

        formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        file_handler.setFormatter(formatter)

        # stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(formatter)

        logger.setLevel(logging.WARNING)
        logger.addHandler(file_handler)
        # logger.addHandler(stream_handler)
        logger.propagate = False

    return logger
