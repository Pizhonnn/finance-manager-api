from fastapi import HTTPException
from app.uow import UnitOfWork
from app.models import User

async def create_user_use_case(uow: UnitOfWork, login: str) -> User:
    existing = await uow.users.get_by_login(login)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(login=login)
    return await uow.users.add(user)