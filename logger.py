import logging
import sys
from pathlib import Path
from config import settings

# Create logs directory
Path("logs").mkdir(exist_ok=True)

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(settings.LOG_LEVEL)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)

# File handler
file_handler = logging.FileHandler('logs/bot.log')
file_handler.setLevel(settings.LOG_LEVEL)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

__all__ = ['logger']
