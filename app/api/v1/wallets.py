from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_db, get_current_user
from app.models import User
from app.schemas import CreateWalletRequest, WalletResponse
from app.uow import UnitOfWork
from app.usecases.create_wallet import create_wallet_use_case
from app.usecases.get_wallets import get_all_wallets_use_case, get_balance_use_case

router = APIRouter()

@router.get("/wallets", response_model=list[WalletResponse])
async def get_all_wallets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    async with UnitOfWork(db) as uow:
        wallets = await get_all_wallets_use_case(uow, current_user.id)
        return [WalletResponse.model_validate(w) for w in wallets]

@router.post("/wallets", response_model=WalletResponse)
async def create_wallet(
    payload: CreateWalletRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    async with UnitOfWork(db) as uow:
        wallet = await create_wallet_use_case(uow, current_user.id, payload)
        return WalletResponse.model_validate(wallet)

@router.get("/balance")
async def get_balance(
    wallet_name: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    async with UnitOfWork(db) as uow:
        return await get_balance_use_case(uow, current_user.id, wallet_name)