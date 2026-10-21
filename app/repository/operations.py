from decimal import Decimal

from sqlalchemy.orm import Session

from app.enum import CurrencyEnum
from app.models import Operation


def create_operation(
    db: Session,
    wallet_id: int,
    type: str,
    amount: Decimal,
    currency: CurrencyEnum,
    category: str | None = None,
    subcategory: str | None = None,
) -> Operation:
    operation = Operation(
        wallet_id=wallet_id,
        type=type,
        amount=amount,
        currency=currency,
        category=category,
        subcategory=subcategory,
    )
    db.add(operation)
    db.flush()  # Без commit!
    db.refresh(operation)
    return operation


def get_operations(db, wallet_ids, date_from=None, date_to=None):
    query = db.query(Operation).filter(Operation.wallet_id.in_(wallet_ids))
    if date_from:
        query = query.filter(Operation.created_at >= date_from)
    if date_to:
        query = query.filter(Operation.created_at <= date_to)
    return query.all()
