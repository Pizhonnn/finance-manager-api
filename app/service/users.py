from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository import users as users_repository
from app.schemas import UserResponse


def create_user(db: Session, login: str):
    existing = users_repository.get_user(db, login)  # ← вызываем с аргументами
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = users_repository.create_user(db, login)
    return UserResponse.model_validate(user)
