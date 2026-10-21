import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Настраиваем логгер
logger = logging.getLogger("api_logger")
logging.basicConfig(level=logging.INFO)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Логируем входящий запрос
        logger.info(f"Request: {request.method} {request.url.path}")

        # Выполняем запрос
        response = await call_next(request)

        # Считаем время выполнения
        process_time = time.time() - start_time

        # Логируем ответ
        logger.info(f"Response: {response.status_code} | Time: {process_time:.4f}s")

        return response
