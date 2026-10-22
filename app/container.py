from config import settings
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from uow import UnitOfWork


class Container(containers.DeclarativeContainer):
    # 1. Настройки (Singleton)
    config = providers.Singleton(lambda: settings)

    # 2. Движок БД (Singleton)
    db_engine = providers.Singleton(
        create_async_engine, config.provided.DATABASE_URL, echo=False
    )

    # Фабрика сессий
    db_session_factory = providers.Singleton(
        async_sessionmaker, bind=db_engine, class_=AsyncSession, expire_on_commit=False
    )

    # Создаем сессию через фабрику (вызываем ее)
    db_session = providers.Factory(
        lambda factory: factory(),  # <-- Вызываем фабрику, чтобы получить AsyncSession
        factory=db_session_factory,
    )

    # UnitOfWork получает уже готовую сессию
    uow = providers.Factory(UnitOfWork, db=db_session)
