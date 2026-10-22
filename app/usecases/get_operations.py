from datetime import datetime

from fastapi import HTTPException
from models import Operation
from uow import UnitOfWork


class GetOperationsListUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(
        self,
        user_id: int,
        wallet_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[Operation]:
        if wallet_id:
            wallet = await self.uow.wallets.get_by_id(wallet_id)
            if not wallet or wallet.user_id != user_id:
                raise HTTPException(
                    status_code=404, detail=f"Wallet '{wallet_id}' not found"
                )
            wallet_ids = [wallet.id]
        else:
            wallets = await self.uow.wallets.get_all_by_user(user_id)
            wallet_ids = [w.id for w in wallets]

        return await self.uow.operations.get_by_wallet_ids(
            wallet_ids, date_from, date_to
        )
