from typing import AsyncGenerator

from database import AsyncSessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    login = credentials.credentials
    result = await db.execute(select(User).where(User.login == login))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
