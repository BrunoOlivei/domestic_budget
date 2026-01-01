from typing import Generator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.core.core import get_settings


class DatabaseConnection:
    _instance: "DatabaseConnection | None" = None
    _engine: Engine | None = None
    _session_factory: sessionmaker | None = None

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._engine is None:
            self._initialize()

    def _initialize(self) -> None:
        settings = get_settings()

        self._engine = create_engine(
            url=str(settings.database_url),
            echo=settings.sqlalchemy_echo,
            pool_size=settings.sqlalchemy_pool_size,
            max_overflow=settings.sqlalchemy_max_overflow,
            pool_pre_ping=True,  # Verify connection before using
        )

        self._session_factory = sessionmaker(
            bind=self._engine,
            class_=Session,
            expire_on_commit=False,
        )

        if "sqlite" in str(settings.database_url):

            @event.listens_for(Engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            self._initialize()
        return self._engine # type: ignore

    @property
    def session_factory(self) -> sessionmaker:
        if self._session_factory is None:
            self._initialize()
        return self._session_factory # type: ignore

    def get_session(self) -> Session:
        if self._session_factory is None:
            self._initialize()
        return self._session_factory() # type: ignore

    def close(self) -> None:
        if self._engine is not None:
            self._engine.dispose()

    @classmethod
    def reset(cls) -> None:
        if cls._instance is not None and cls._instance._engine is not None:
            cls._instance.close()
        cls._instance = None
        cls._engine = None
        cls._session_factory = None


_database = DatabaseConnection()


def get_database() -> DatabaseConnection:
    return _database


async def get_db_session() -> Generator[Session, None, None]: # type: ignore
    session = _database.get_session()
    try:
        yield session # type: ignore
    finally:
        session.close()
