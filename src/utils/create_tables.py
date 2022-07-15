from loguru import logger

from src.models import Base

from .session_manager import engine


async def create_tables():
    async with engine.begin() as conn:
        logger.info("Creating tables if not exist")
        await conn.run_sync(Base.metadata.create_all)  # type: ignore
