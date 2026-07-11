from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.logger import configure_logger, logger
from app.db.database import db
from app.redis.redis import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown.
    """

    # Configure Logging
    configure_logger()
    logger.info("Starting Gymtik...")

    # Verify PostgreSQL
    try:
        with db.session() as session:
            session.execute(text("SELECT 1"))

        logger.info("PostgreSQL connection established.")
    except Exception as exc:
        logger.exception("Failed to connect to PostgreSQL.", error=str(exc))
        raise
    

    # Verify Redis
    try:
        if not redis.ping():
            raise RuntimeError("Redis ping failed.")
        logger.info("Redis connection established.")
    except Exception as exc:
        logger.exception("Failed to connect to Redis.", error=str(exc))
        raise

    logger.info("Application startup completed.")
    yield

    logger.info("Application shutting down...")

    redis.close()
    db.dispose()

    logger.info("Resources released successfully.")