import os
import logging

def get_logger(name: str) -> logging.Logger:
    # Docker-friendly log directory
    log_dir = os.environ.get("LOG_DIR", "/app/logs")
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)

    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(f"{log_dir}/{name}.log")
        file_handler.setLevel(logging.INFO)  # Capture INFO+ messages
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Stream handler for Docker logs
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        logger.setLevel(logging.INFO)
        logger.propagate = False

    return logger
