from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


class Database:
    """
    Central database manager responsible for creating the SQLAlchemy
    engine and providing database sessions.
    """

    def __init__(self) -> None:
        self._engine: Engine = create_engine(
            url=settings.database.url,
            pool_pre_ping=True,
            pool_size=settings.database.pool_size,
            max_overflow=settings.database.max_overflow,
            pool_timeout=settings.database.pool_timeout,
            echo=settings.is_development,
        )

        self._session_factory = sessionmaker(
            bind=self._engine,
            class_=Session,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> Engine:
        """
        Returns the SQLAlchemy engine.
        """
        return self._engine

    def get_session(self) -> Generator[Session, None, None]:
        """
        Dependency for FastAPI routes.
        Creates a database session and closes it automatically.
        """
        session = self._session_factory()

        try:
            yield session
        finally:
            session.close()

    def dispose(self) -> None:
        """
        Gracefully disposes the engine and closes all pooled connections.
        """
        self._engine.dispose()
        
    def session(self) -> Session:
        return self._session_factory()
    


db = Database()
def get_db() -> Generator[Session, None, None]:
    session = db.session()

    try:
        yield session
    finally:
        session.close()