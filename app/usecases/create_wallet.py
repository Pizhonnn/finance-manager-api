from fastapi import HTTPException
from models import Wallet
from schemas import CreateWalletRequest
from uow import UnitOfWork


class CreateWalletUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, user_id: int, data: CreateWalletRequest) -> Wallet:
        existing = await self.uow.wallets.get_by_name_and_user(user_id, data.name)
        if existing:
            raise HTTPException(status_code=409, detail="Wallet already exists")

        return await self.uow.wallets.create(
            user_id=user_id,
            name=data.name,
            amount=data.initial_balance,
            currency=data.currency,
        )
