from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.repository import wallets as wallets_repository
from app.schemas import CreateWalletRequest, WalletResponse


def get_wallet(db: Session, current_user: User, wallet_name: str | None = None):
    # Если имя не указано — сумма всех
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets(db, current_user.id)
        return {"total_balance": sum(w.amount for w in wallets)}

    # Проверяем существует ли кошелёк
    if not wallets_repository.is_wallet_exist(db, current_user.id, wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found",
        )

    # Возвращаем баланс
    wallet = wallets_repository.get_wallets_balance_by_name(
        db, current_user.id, wallet_name
    )
    return {"wallet": wallet.name, "balance": wallet.amount}


# Сервис создания кошелька
def create_wallet(
    wallet: CreateWalletRequest, db: Session, current_user: User
) -> WalletResponse:
    # Проверяем, есть ли уже кошелёк с таким именем у ТЕКУЩЕГО юзера
    # is_wallet_exist(db, user_id, wallet_name) — три аргумента
    if wallets_repository.is_wallet_exist(db, current_user.id, wallet.name):
        raise HTTPException(
            status_code=409,
            detail=f"Wallet '{wallet.name}' already exists",
        )

    # Создаём кошелёк в БД, привязывая его к текущему юзеру
    created = wallets_repository.create_wallet(
        db,
        current_user.id,  # id владельца
        wallet.name,  # имя кошелька из схемы
        wallet.initial_balance,  # начальный баланс из схемы
        wallet.currency,
    )

    # Возвращаем ответ — берём данные из созданного объекта
    return WalletResponse.model_validate(created)

def get_all_wallets(db: Session, current_user: User):
    # Просто передаем управление в репозиторий
    return wallets_repository.get_all_wallets(db, current_user.id)