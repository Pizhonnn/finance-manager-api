from datetime import datetime

from container import Container
from dependency import get_current_user
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from models import User
from schemas import OperationRequest, OperationResponse
from uow import UnitOfWork
from usecases.create_operation import AddExpenseUseCase, AddIncomeUseCase
from usecases.get_operations import GetOperationsListUseCase

router = APIRouter()


@router.post(
    "/operations/income", response_model=OperationResponse, operation_id="add_income"
)
@inject
async def add_income(
    payload: OperationRequest,
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
):
    async with uow:
        use_case = AddIncomeUseCase(uow)
        operation = await use_case.execute(current_user.id, payload)
        return OperationResponse.model_validate(operation)


@router.post(
    "/operations/expense", response_model=OperationResponse, operation_id="add_expense"
)
@inject
async def add_expense(
    payload: OperationRequest,
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
):
    async with uow:
        use_case = AddExpenseUseCase(uow)
        operation = await use_case.execute(current_user.id, payload)
        return OperationResponse.model_validate(operation)


@router.get(
    "/operations", response_model=list[OperationResponse], operation_id="get_operations"
)
@inject
async def get_operations(
    wallet_id: int | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
):
    async with uow:
        use_case = GetOperationsListUseCase(uow)
        operations = await use_case.execute(
            current_user.id, wallet_id, date_from, date_to
        )
        return [OperationResponse.model_validate(op) for op in operations]
