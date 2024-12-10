from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

DATABASE_URL = settings.database_url

# Создание асинхронного движка базы данных
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Асинхронная сессия
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session




