from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.models import Operation
from app.repository.base import AbstractRepository

class OperationRepository(AbstractRepository[Operation]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, operation: Operation) -> Operation:
        self.db.add(operation)
        await self.db.flush()
        return operation

    async def get(self, entity_id: int) -> Operation | None:
        result = await self.db.execute(select(Operation).where(Operation.id == entity_id))
        return result.scalar_one_or_none()

    async def get_by_wallet_ids(self, wallet_ids: list[int], date_from: datetime | None = None, date_to: datetime | None = None) -> list[Operation]:
        query = select(Operation).where(Operation.wallet_id.in_(wallet_ids))
        if date_from:
            query = query.where(Operation.created_at >= date_from)
        if date_to:
            query = query.where(Operation.created_at <= date_to)
        result = await self.db.execute(query)
        return list(result.scalars().all())