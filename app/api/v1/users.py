from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_db, get_current_user
from app.models import User
from app.schemas import UserRequest, UserResponse
from app.uow import UnitOfWork
from app.usecases.create_user import create_user_use_case

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(payload: UserRequest, db: AsyncSession = Depends(get_db)):
    async with UnitOfWork(db) as uow:
        user = await create_user_use_case(uow, payload.login)
        return UserResponse.model_validate(user)

@router.get("/users.me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)