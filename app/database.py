from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Создаем асинхронный движок
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()
