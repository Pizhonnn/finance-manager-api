from datetime import datetime

from models import Operation
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class OperationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, operation: Operation) -> Operation:
        self.db.add(operation)
        await self.db.flush()
        return operation

    async def get_by_wallet_ids(
        self,
        wallet_ids: list[int],
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[Operation]:
        query = select(Operation).where(Operation.wallet_id.in_(wallet_ids))
        if date_from:
            query = query.where(Operation.created_at >= date_from)
        if date_to:
            query = query.where(Operation.created_at <= date_to)
        result = await self.db.execute(query)
        return list(result.scalars().all())
