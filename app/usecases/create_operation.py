from fastapi import HTTPException
from app.uow import UnitOfWork
from app.schemas import OperationRequest, OperationResponse
from app.models import Operation

async def add_income_use_case(uow: UnitOfWork, user_id: int, data: OperationRequest) -> Operation:
    wallet = await uow.wallets.get_by_name_and_user(user_id, data.wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail=f"Wallet '{data.wallet_name}' not found")

    wallet.amount += data.amount

    operation = Operation(
        wallet_id=wallet.id,
        type="income",
        amount=data.amount,
        currency=wallet.currency,
        category=data.description,
    )
    return await uow.operations.add(operation)

async def add_expense_use_case(uow: UnitOfWork, user_id: int, data: OperationRequest) -> Operation:
    wallet = await uow.wallets.get_by_name_and_user(user_id, data.wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail=f"Wallet '{data.wallet_name}' not found")

    if wallet.amount < data.amount:
        raise HTTPException(status_code=400, detail=f"Insufficient funds. Available: {wallet.amount}")

    wallet.amount -= data.amount

    operation = Operation(
        wallet_id=wallet.id,
        type="expense",
        amount=data.amount,
        currency=wallet.currency,
        category=data.description,
    )
    return await uow.operations.add(operation)

async def get_operations_list_use_case(
    uow: UnitOfWork,
    user_id: int,
    wallet_id: int | None = None,
    date_from=None,
    date_to=None
) -> list[Operation]:
    if wallet_id:
        wallet = await uow.wallets.get(wallet_id) # Проверка владельца упущена для краткости, лучше добавить
        if not wallet or wallet.user_id != user_id:
            raise HTTPException(status_code=404, detail=f"Wallet '{wallet_id}' not found")
        wallet_ids = [wallet.id]
    else:
        wallets = await uow.wallets.get_all_by_user(user_id)
        wallet_ids = [w.id for w in wallets]

    return await uow.operations.get_by_wallet_ids(wallet_ids, date_from, date_to)