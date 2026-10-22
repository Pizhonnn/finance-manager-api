from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal
from app.models import Wallet
from app.enum import CurrencyEnum
from app.repository.base import AbstractRepository

class WalletRepository(AbstractRepository[Wallet]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name_and_user(self, user_id: int, name: str) -> Wallet | None:
        result = await self.db.execute(
            select(Wallet).where(Wallet.name == name, Wallet.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all_by_user(self, user_id: int) -> list[Wallet]:
        result = await self.db.execute(select(Wallet).where(Wallet.user_id == user_id))
        return list(result.scalars().all())

    async def add(self, wallet: Wallet) -> Wallet:
        self.db.add(wallet)
        await self.db.flush()
        return wallet

    async def get(self, entity_id: int) -> Wallet | None:
        result = await self.db.execute(select(Wallet).where(Wallet.id == entity_id))
        return result.scalar_one_or_none()