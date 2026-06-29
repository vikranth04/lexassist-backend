import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url.path}")
        start_time = time.time()
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            logger.info(
                f"Response: status={response.status_code} "
                f"path={request.url.path} duration={duration:.4f}s"
            )
            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Exception: path={request.url.path} "
                f"error={str(e)} duration={duration:.4f}s"
            )
            raise e
