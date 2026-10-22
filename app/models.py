from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.enums import CurrencyEnum


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    amount: Mapped[Decimal] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    currency: Mapped[CurrencyEnum]


class Operation(Base):
    __tablename__ = "operation"

    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallet.id"))
    type: Mapped[str]
    amount: Mapped[Decimal]
    currency: Mapped[CurrencyEnum]
    category: Mapped[str | None] = mapped_column(default=None)  # ← добавить
    subcategory: Mapped[str | None] = mapped_column(default=None)  # ← добавить
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
