from api.v1.router import api_router
from container import Container
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from middleware import LoggingMiddleware

app = FastAPI(
    title="Finance API",
    description="Сервис для управления кошельками и операциями",
    version="1.0.0",
)
app.add_middleware(LoggingMiddleware)

container = Container()
container.wire(modules=["api.v1.users", "api.v1.wallets", "api.v1.operations"])

app.include_router(api_router, prefix="/api/v1")

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return FileResponse("static/index.html")
