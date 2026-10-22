from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
from app.repository.base import AbstractRepository

class UserRepository(AbstractRepository[User]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_login(self, login: str) -> User | None:
        result = await self.db.execute(select(User).where(User.login == login))
        return result.scalar_one_or_none()

    async def add(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush() # flush, чтобы получить id, но не коммитить
        return user

    async def get(self, entity_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == entity_id))
        return result.scalar_one_or_none()