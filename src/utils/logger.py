import logging
import os

def setup_logger(name: str = "trading_bot") -> logging.Logger:
    """
    Configures and returns a logger instance.
    Logs to both console and file (logs/app.log).
    """

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs if multiple imports occur
    if logger.hasHandlers():
        return logger

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File Handler
    file_handler = logging.FileHandler(f"{log_dir}/app.log")
    file_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add Handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Default logger instance
logger = setup_logger()
