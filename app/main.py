from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.operations import router as operations_router
from app.api.v1.users import router as users_router

# Импортируем роутеры
from app.api.v1.wallets import router as wallet_router
from app.middleware import LoggingMiddleware

# Создаём экземпляр приложения FastAPI
app = FastAPI(
    title="Finance API",
    description="Сервис для управления кошельками и операциями",
    version="1.0.0",
)
app.add_middleware(LoggingMiddleware)
# Подключаем роутеры с префиксом /api/v1
app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(wallet_router, prefix="/api/v1", tags=["wallet"])
app.include_router(operations_router, prefix="/api/v1", tags=["operations"])


@app.get("/health", tags=["health"])
def health_check():
    """
    Эндпоинт для проверки работоспособности сервиса.
    Используется в Docker healthcheck и на продакшене.
    """
    return {"status": "ok"}

# Монтируем папку static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Отдаем index.html на корневой запрос
@app.get("/")
def read_root():
    return FileResponse("static/index.html")
