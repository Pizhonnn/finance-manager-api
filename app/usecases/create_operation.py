from fastapi import HTTPException

from models import Operation
from schemas import OperationRequest
from uow import UnitOfWork


class AddIncomeUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, user_id: int, data: OperationRequest) -> Operation:
        wallet = await self.uow.wallets.get_domain_by_name_and_user(
            user_id, data.wallet_name
        )
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{data.wallet_name}' not found",
            )


        wallet.add_income(data.amount)
        await self.uow.wallets.save_domain(wallet)

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
        wallet = await self.uow.wallets.get_domain_by_name_and_user(
            user_id, data.wallet_name
        )
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{data.wallet_name}' not found",
            )

        try:
            wallet.add_expense(data.amount)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        await self.uow.wallets.save_domain(wallet)

        operation = Operation(
            wallet_id=wallet.id,
            type="expense",
            amount=data.amount,
            currency=wallet.currency,
            category=data.description,
        )
        return await self.uow.operations.create(operation)