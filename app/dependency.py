from typing import Generator

# Импортируем Depends (для DI), HTTPException (для ошибок), status (для статус-кодов)
from fastapi import Depends, HTTPException, status

# HTTPBearer — извлекает токен из заголовка Authorization
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Session — класс для работы с сессией SQLAlchemy
from sqlalchemy.orm import Session

# Фабрика сессий из нашего проекта
from app.database import SessionLocal

# Модель User из ORM — чтобы указать тип возврата
from app.models import User

# Репозиторий пользователей — для поиска user в БД
from app.repository import users as users_repository

# Объект HTTPBearer — извлекает токен из заголовка "Authorization: Bearer ..."
security = HTTPBearer()


# Функция для получения сессии базы данных через dependency injection в FastAPI
def get_db() -> Generator[Session, None, None]:
    # Создаём новую сессию для работы с базой данных
    db = SessionLocal()
    try:
        # Возвращаем сессию через yield (FastAPI управляет ей)
        yield db
    finally:
        # Закрываем сессию в любом случае — даже если была ошибка
        db.close()


# Функция для получения текущего пользователя по JWT-токену
def get_current_user(
    # Токен из заголовка Authorization (Bearer ...)
    credentials: HTTPAuthorizationCredentials = Depends(security),
    # Сессия БД через DI
    db: Session = Depends(get_db),
) -> User:
    # Достаём сам токен (уже без слова "Bearer")
    login = credentials.credentials

    # Ищем пользователя в БД по токену
    user = users_repository.get_user(db, login)

    # Если не нашли — токен невалидный, возвращаем 401
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    # Возвращаем найденного пользователя — он попадёт в эндпоинт
    return user
