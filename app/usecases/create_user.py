from fastapi import HTTPException
from models import User
from uow import UnitOfWork


class CreateUserUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, login: str) -> User:
        existing = await self.uow.users.get_by_login(login)
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        return await self.uow.users.create(login)
