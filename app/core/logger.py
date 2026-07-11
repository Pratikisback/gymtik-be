import logging
import sys

import structlog

from app.core.config import settings


def configure_logger() -> None:
    """
    Configure the application's structured logger.
    """

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    logging.basicConfig(
        level=getattr(logging, settings.logging.level),
        format="%(message)s",
        stream=sys.stdout,
    )

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


logger = structlog.get_logger()