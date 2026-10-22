from container import Container
from dependency import get_current_user
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from models import User
from schemas import UserRequest, UserResponse
from uow import UnitOfWork
from usecases.create_user import CreateUserUseCase

router = APIRouter()


@router.post("/users", response_model=UserResponse, operation_id="create_user")
@inject
async def create_user(
    payload: UserRequest, uow: UnitOfWork = Depends(Provide[Container.uow])
):
    async with uow:
        use_case = CreateUserUseCase(uow)
        user = await use_case.execute(payload.login)
        return UserResponse.model_validate(user)


@router.get("/users.me", response_model=UserResponse, operation_id="get_me")
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
