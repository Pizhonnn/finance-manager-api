from decimal import Decimal

from enums import CurrencyEnum
from models import Wallet
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class WalletRepository:
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

    async def create(
        self, user_id: int, name: str, amount: Decimal, currency: CurrencyEnum
    ) -> Wallet:
        wallet = Wallet(name=name, amount=amount, user_id=user_id, currency=currency)
        self.db.add(wallet)
        await self.db.flush()
        return wallet

    async def get_by_id(self, wallet_id: int) -> Wallet | None:
        result = await self.db.execute(select(Wallet).where(Wallet.id == wallet_id))
        return result.scalar_one_or_none()
