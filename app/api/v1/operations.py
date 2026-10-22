from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_db, get_current_user
from app.models import User
from app.schemas import OperationRequest, OperationResponse
from app.uow import UnitOfWork
from app.usecases.create_operation import (
    add_income_use_case,
    add_expense_use_case,
    get_operations_list_use_case,
)

router = APIRouter()

@router.post("/operations/income", response_model=OperationResponse)
async def add_income(
    payload: OperationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    async with UnitOfWork(db) as uow:
        operation = await add_income_use_case(uow, current_user.id, payload)
        return OperationResponse.model_validate(operation)

@router.post("/operations/expense", response_model=OperationResponse)
async def add_expense(
    payload: OperationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    async with UnitOfWork(db) as uow:
        operation = await add_expense_use_case(uow, current_user.id, payload)
        return OperationResponse.model_validate(operation)

@router.get("/operations", response_model=list[OperationResponse])
async def get_operations(
    wallet_id: int | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    async with UnitOfWork(db) as uow:
        operations = await get_operations_list_use_case(
            uow, current_user.id, wallet_id, date_from, date_to
        )
        return [OperationResponse.model_validate(op) for op in operations]