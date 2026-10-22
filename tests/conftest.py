from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.dependency import get_db
from app.main import app

# Используем SQLite в памяти (быстро и без файлов)
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Важно! Чтобы все соединения видели одну базу
)

TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)


def get_test_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Переопределяем зависимость глобально
app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope="function")
def client():
    # Перед тестом создаем таблицы
    Base.metadata.create_all(bind=test_engine)
    with TestClient(app) as c:
        yield c
    # После теста удаляем таблицы
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
