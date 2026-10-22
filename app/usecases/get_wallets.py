from fastapi import HTTPException
from app.uow import UnitOfWork
from app.schemas import WalletResponse
from app.models import Wallet

async def get_all_wallets_use_case(uow: UnitOfWork, user_id: int) -> list[Wallet]:
    return await uow.wallets.get_all_by_user(user_id)

async def get_balance_use_case(uow: UnitOfWork, user_id: int, wallet_name: str | None = None):
    if wallet_name:
        wallet = await uow.wallets.get_by_name_and_user(user_id, wallet_name)
        if not wallet:
            raise HTTPException(status_code=404, detail=f"Wallet '{wallet_name}' not found")
        return {"wallet": wallet.name, "balance": wallet.amount}
    else:
        wallets = await uow.wallets.get_all_by_user(user_id)
        total = sum(w.amount for w in wallets)
        return {"total_balance": total}