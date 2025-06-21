# reddit_scraper/logging_setup.py
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """
    Configure root logger with a console handler and an optional rotating file handler.

    level     ─ "DEBUG", "INFO", "WARNING", "ERROR", or "CRITICAL"
    log_file  ─ path to a logfile; if omitted, logs stay in the console only.
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    fmt = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3))

    logging.basicConfig(level=numeric_level, format=fmt, datefmt=datefmt, handlers=handlers)
