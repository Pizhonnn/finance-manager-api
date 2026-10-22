from container import Container
from dependency import get_current_user
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from models import User
from schemas import CreateWalletRequest, WalletResponse
from uow import UnitOfWork
from usecases.create_wallet import CreateWalletUseCase
from usecases.get_wallets import GetAllWalletsUseCase, GetBalanceUseCase

router = APIRouter()


@router.get(
    "/wallets", response_model=list[WalletResponse], operation_id="get_all_wallets"
)
@inject
async def get_all_wallets(
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
):
    async with uow:
        use_case = GetAllWalletsUseCase(uow)
        wallets = await use_case.execute(current_user.id)
        return [WalletResponse.model_validate(w) for w in wallets]


@router.post("/wallets", response_model=WalletResponse, operation_id="create_wallet")
@inject
async def create_wallet(
    payload: CreateWalletRequest,
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
):
    async with uow:
        use_case = CreateWalletUseCase(uow)
        wallet = await use_case.execute(current_user.id, payload)
        return WalletResponse.model_validate(wallet)


@router.get("/balance", operation_id="get_balance")
@inject
async def get_balance(
    wallet_name: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
):
    async with uow:
        use_case = GetBalanceUseCase(uow)
        return await use_case.execute(current_user.id, wallet_name)
