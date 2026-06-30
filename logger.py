"""
Alpha Bot — Logging setup with colorlog for console + file output.
"""
import logging
import logging.handlers
import os
from pathlib import Path


def setup_logging(log_level: str = "INFO"):
    Path("logs").mkdir(exist_ok=True)

    fmt_console = "%(log_color)s%(asctime)s [%(levelname)s]%(reset)s %(name)s — %(message)s"
    fmt_file = "%(asctime)s [%(levelname)s] %(name)s — %(message)s"

    # Console handler (colorlog)
    try:
        import colorlog
        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(colorlog.ColoredFormatter(
            fmt_console,
            datefmt="%H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            }
        ))
    except ImportError:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s — %(message)s", datefmt="%H:%M:%S"
        ))

    # Rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        "logs/alpha_bot.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter(fmt_file))

    # Error-only file handler
    error_handler = logging.handlers.RotatingFileHandler(
        "logs/errors.log",
        maxBytes=2 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(fmt_file))

    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(level=level, handlers=[console_handler, file_handler, error_handler])

    # Silence noisy third-party loggers
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
