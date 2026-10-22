from fastapi import APIRouter

from app.api.v1.users import router as users_router
from app.api.v1.wallets import router as wallets_router
from app.api.v1.operations import router as operations_router

# Собираем все роутеры версии v1 в один
api_router = APIRouter()

api_router.include_router(users_router, tags=["users"])
api_router.include_router(wallets_router, tags=["wallet"])
api_router.include_router(operations_router, tags=["operations"])