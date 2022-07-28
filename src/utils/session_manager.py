from typing import Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER

engine = create_async_engine(
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}",
    execution_options={"isolation_level": "SERIALIZABLE"},
    echo=True,
)


AsyncSession: _AsyncSession = sessionmaker(
    engine,
    class_=_AsyncSession,  # type: ignore
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class SessionManager:
    def __init__(self, session: Optional[_AsyncSession] = None):
        self.session = session or AsyncSession()  # type: ignore
        self.autoclose = session is None

    async def __aenter__(self) -> _AsyncSession:
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            await self.session.rollback()
            logger.exception(exc)
            return

        await self.session.commit()
        if self.autoclose:
            await self.session.close()
