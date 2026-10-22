from repository.operations import OperationRepository
from repository.users import UserRepository
from repository.wallets import WalletRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)
        self.wallets = WalletRepository(db)
        self.operations = OperationRepository(db)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.db.rollback()
        else:
            await self.db.commit()
        await self.db.close()
