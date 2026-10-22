from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.v1.router import api_router
from app.middleware import LoggingMiddleware

app = FastAPI(
    title="Finance API",
    description="Сервис для управления кошельками и операциями",
    version="1.0.0",
)
app.add_middleware(LoggingMiddleware)

# Подключаем ВСЕ эндпоинты v1 одной строкой
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")