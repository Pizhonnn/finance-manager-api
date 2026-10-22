from models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_login(self, login: str) -> User | None:
        result = await self.db.execute(select(User).where(User.login == login))
        return result.scalar_one_or_none()

    async def create(self, login: str) -> User:
        user = User(login=login)
        self.db.add(user)
        await self.db.flush()
        return user
