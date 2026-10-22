from fastapi import HTTPException
from models import Operation
from schemas import OperationRequest
from uow import UnitOfWork


class AddIncomeUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, user_id: int, data: OperationRequest) -> Operation:
        wallet = await self.uow.wallets.get_by_name_and_user(user_id, data.wallet_name)
        if not wallet:
            raise HTTPException(
                status_code=404, detail=f"Wallet '{data.wallet_name}' not found"
            )

        wallet.amount += data.amount
        operation = Operation(
            wallet_id=wallet.id,
            type="income",
            amount=data.amount,
            currency=wallet.currency,
            category=data.description,
        )
        return await self.uow.operations.create(operation)


class AddExpenseUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, user_id: int, data: OperationRequest) -> Operation:
        wallet = await self.uow.wallets.get_by_name_and_user(user_id, data.wallet_name)
        if not wallet:
            raise HTTPException(
                status_code=404, detail=f"Wallet '{data.wallet_name}' not found"
            )

        if wallet.amount < data.amount:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient funds. Available: {wallet.amount}",
            )

        wallet.amount -= data.amount
        operation = Operation(
            wallet_id=wallet.id,
            type="expense",
            amount=data.amount,
            currency=wallet.currency,
            category=data.description,
        )
        return await self.uow.operations.create(operation)
