from fastapi import HTTPException
from models import Wallet
from uow import UnitOfWork


class GetAllWalletsUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, user_id: int) -> list[Wallet]:
        return await self.uow.wallets.get_all_by_user(user_id)


class GetBalanceUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, user_id: int, wallet_name: str | None = None):
        if wallet_name:
            wallet = await self.uow.wallets.get_by_name_and_user(user_id, wallet_name)
            if not wallet:
                raise HTTPException(
                    status_code=404, detail=f"Wallet '{wallet_name}' not found"
                )
            return {"wallet": wallet.name, "balance": wallet.amount}
        else:
            wallets = await self.uow.wallets.get_all_by_user(user_id)
            total = sum(w.amount for w in wallets)
            return {"total_balance": total}
