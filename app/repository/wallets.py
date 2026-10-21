from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enum import CurrencyEnum
from app.models import Wallet


def is_wallet_exist(db: Session, user_id: int, wallet_name: str) -> bool:
    return (
        db.query(Wallet)
        .filter(Wallet.name == wallet_name, Wallet.user_id == user_id)
        .first()
        is not None
    )


def add_income(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    stmt = select(Wallet).where(Wallet.name == wallet_name, Wallet.user_id == user_id)
    wallet = db.execute(stmt).scalar_one()

    wallet.amount += amount
    db.flush()  # Фиксируем изменения в транзакции, но не коммитим
    return wallet


def add_expense(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    stmt = select(Wallet).where(Wallet.name == wallet_name, Wallet.user_id == user_id)
    wallet = db.execute(stmt).scalar_one()

    # Проверка на достаточность средств
    if wallet.amount < amount:
        raise ValueError("Insufficient funds")

    wallet.amount -= amount
    db.flush()
    return wallet


def get_wallets_balance_by_name(db: Session, user_id: int, wallet_name: str) -> Wallet:
    stmt = select(Wallet).where(Wallet.name == wallet_name, Wallet.user_id == user_id)
    return db.execute(stmt).scalar_one()


def get_all_wallets(db: Session, user_id: int) -> list[Wallet]:
    stmt = select(Wallet).where(Wallet.user_id == user_id)
    return list(db.execute(stmt).scalars().all())


def get_wallet_by_id(db: Session, user_id: int, wallet_id: int) -> Wallet | None:
    return (
        db.query(Wallet)
        .filter(Wallet.id == wallet_id, Wallet.user_id == user_id)
        .first()
    )


def create_wallet(
    db: Session,
    user_id: int,
    wallet_name: str,
    amount: Decimal,
    currency: CurrencyEnum,
) -> Wallet:
    wallet = Wallet(
        name=wallet_name,
        amount=amount,
        user_id=user_id,
        currency=currency,
    )
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet
