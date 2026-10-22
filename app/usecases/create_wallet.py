from fastapi import HTTPException
from app.uow import UnitOfWork
from app.schemas import CreateWalletRequest
from app.models import Wallet

async def create_wallet_use_case(uow: UnitOfWork, user_id: int, data: CreateWalletRequest) -> Wallet:
    existing = await uow.wallets.get_by_name_and_user(user_id, data.name)
    if existing:
        raise HTTPException(status_code=409, detail="Wallet already exists")

    wallet = Wallet(
        name=data.name,
        amount=data.initial_balance,
        user_id=user_id,
        currency=data.currency
    )
    return await uow.wallets.add(wallet)