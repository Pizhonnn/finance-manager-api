from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.enum import CurrencyEnum

# --- СХЕМЫ ДЛЯ ПОЛЬЗОВАТЕЛЯ ---


class UserRequest(BaseModel):
    """Схема запроса для регистрации пользователя."""

    login: str = Field(..., max_length=127)


class UserResponse(UserRequest):
    """Схема ответа для пользователя."""

    model_config = {"from_attributes": True}
    id: int


# --- СХЕМЫ ДЛЯ КОШЕЛЬКА ---

class CreateWalletRequest(BaseModel):
    """Схема запроса для создания кошелька."""

    name: str = Field(..., max_length=127)
    initial_balance: Decimal = Field(default=Decimal("0.00"), ge=0)
    currency: CurrencyEnum = CurrencyEnum.RUB

    @field_validator("name")
    @classmethod
    def name_is_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Wallet name cannot be empty")
        return v


class WalletResponse(BaseModel):  # <-- ВЫНЕСИ ЕГО НА УРОВЕНЬ МОДУЛЯ (без отступа)
    """Схема ответа для кошелька."""
    model_config = {"from_attributes": True}
    id: int
    name: str
    amount: Decimal
    currency: CurrencyEnum

# --- СХЕМЫ ДЛЯ ОПЕРАЦИЙ (ПРИХОД/РАСХОД) ---

class OperationRequest(BaseModel):
    """Схема запроса для операций (приход/расход)."""

    wallet_name: str = Field(..., max_length=127)
    # Используем Decimal, чтобы не было потери копеек
    amount: Decimal
    description: str | None = Field(None, max_length=255)

    @field_validator("amount")
    @classmethod
    def amount_is_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v

    @field_validator("wallet_name")
    @classmethod
    def wallet_name_is_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Wallet name cannot be empty")
        return v


class OperationResponse(BaseModel):
    """Схема ответа для операции."""

    model_config = {"from_attributes": True}
    id: int
    wallet_id: int
    type: str
    amount: Decimal
    currency: CurrencyEnum
    category: str | None
    subcategory: str | None
    created_at: datetime
