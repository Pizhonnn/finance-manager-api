from decimal import Decimal
from app.enum import CurrencyEnum
from app.models import User, Wallet


def test_add_expense_success(db_session, client):
    # Arrange Подготовка данных
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(
        name="card",
        amount=200,
        user_id=user.id,
        currency=CurrencyEnum.RUB
    )
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # Act
    response = client.post(
        "/api/v1/operations/expense",
        json={"wallet_name": "card", "amount": 50.0, "description": "food"},
        headers={"Authorization": f"Bearer {user.login}"},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "expense"
    assert Decimal(str(data["amount"])) == Decimal("50.0")
    assert data["wallet_id"] == wallet.id
    assert data["category"] == "food"


def test_add_expense_negative_amount(db_session, client):
    # Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(
        name="card",
        amount=100,
        user_id=user.id,
        currency=CurrencyEnum.RUB
    )
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # Act
    response = client.post(
        "/api/v1/operations/expense",
        json={"wallet_name": "    ", "amount": 50.0, "description": "food"},
        headers={"Authorization": f"Bearer {user.login}"},
    )

    # Assert
    assert response.status_code == 422