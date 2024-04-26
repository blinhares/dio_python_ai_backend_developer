from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from workout_api.src.config.settings import settings

engine = create_async_engine(
    settings.DB_URL,
    echo=False)

async_session = sessionmaker(
    engine, # type: ignore
    class_=AsyncSession,
    expire_on_commit=False)

async def get_session() -> AsyncGenerator: # type: ignore
    async with async_session() as session: # type: ignore
        yield session