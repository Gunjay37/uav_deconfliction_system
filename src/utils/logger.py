"""
Logging utilities for the deconfliction system.
"""
import logging
import os
from src.utils.config import get_config

config = get_config()

# Create logs directory if needed
os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)