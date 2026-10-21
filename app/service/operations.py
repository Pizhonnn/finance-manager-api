from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.repository import operations as operations_repository
from app.repository import wallets as wallets_repository
from app.schemas import OperationRequest, OperationResponse


def add_income(
    db: Session, current_user: User, data: OperationRequest
) -> OperationResponse:
    # Проверяем существует ли кошелёк
    if not wallets_repository.is_wallet_exist(db, current_user.id, data.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{data.wallet_name}' not found",
        )

    # Добавляем доход
    wallet = wallets_repository.add_income(
        db,
        current_user.id,
        data.wallet_name,
        data.amount,  # Теперь это Decimal благодаря схеме
    )

    # Создаём запись об операции
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type="income",
        amount=data.amount,
        currency=wallet.currency,
        category=data.description,
    )

    # ОДИН commit — либо оба изменения, либо ни одного
    db.commit()

    return OperationResponse.model_validate(operation)


def add_expense(
    db: Session, current_user: User, data: OperationRequest
) -> OperationResponse:
    # Проверяем существует ли кошелёк
    if not wallets_repository.is_wallet_exist(db, current_user.id, data.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{data.wallet_name}' not found",
        )

    # Получаем кошелёк для проверки баланса
    wallet = wallets_repository.get_wallets_balance_by_name(
        db, current_user.id, data.wallet_name
    )

    # Проверяем, что денег хватает (сравнение Decimal)
    if wallet.amount < data.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {wallet.amount}",
        )

    # Списываем расход
    wallet = wallets_repository.add_expense(
        db,
        current_user.id,
        data.wallet_name,
        data.amount,
    )

    # Создаём запись об операции
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type="expense",
        amount=data.amount,
        currency=wallet.currency,
        category=data.description,
    )

    db.commit()
    return OperationResponse.model_validate(operation)


def get_operations_list(
    db: Session,
    current_user: User,
    wallet_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[OperationResponse]:
    if wallet_id:
        wallet = wallets_repository.get_wallet_by_id(db, current_user.id, wallet_id)
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{wallet_id}' not found",
            )
        wallet_ids = [wallet.id]
    else:
        wallets = wallets_repository.get_all_wallets(db, current_user.id)
        wallet_ids = [w.id for w in wallets]

    operations = operations_repository.get_operations(
        db,
        wallet_ids,
        date_from,
        date_to,
    )

    return [OperationResponse.model_validate(op) for op in operations]
