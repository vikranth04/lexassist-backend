# pyrefly: ignore [missing-import]
import os
import sys
from loguru import logger

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

logger.add(
    "logs/backend.log",
    rotation="5 MB",
    retention="10 days",
    level="INFO"
)
