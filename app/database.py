import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Берем URL из окружения (для Docker).
# Если нет — используем локальный Postgres по умолчанию
# Обрати внимание на порт 15432 (мы пробрасывали его в Docker Compose)
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
)

# Создаем движок. Для Postgres параметры check_same_thread не нужны.
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()
