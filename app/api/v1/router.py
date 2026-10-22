from api.v1.operations import router as operations_router
from api.v1.users import router as users_router
from api.v1.wallets import router as wallets_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(users_router, tags=["users"])
api_router.include_router(wallets_router, tags=["wallet"])
api_router.include_router(operations_router, tags=["operations"])
