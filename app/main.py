import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import (
    health,
    website,
    chat,
    conversation,
    sources,
    pdf
)
from app.middleware.cors import setup_cors
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_time import RequestTimeMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.core.exceptions import (
    AppBaseException,
    app_exception_handler,
    general_exception_handler
)
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    logger.info("Executing startup validation sequences...")
    for path in ["app/storage/uploads", "app/storage/processed", "app/storage/temp"]:
        os.makedirs(path, exist_ok=True)
        logger.info(f"Verified storage path: {path}")
    logger.info("Startup validation sequence successfully completed.")
    yield
    # Shutdown tasks
    logger.info("Executing graceful shutdown sequence...")
    temp_dir = "app/storage/temp"
    if os.path.exists(temp_dir):
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.error(f"Failed to delete temporary file {file_path}: {e}")
    logger.info("Graceful shutdown completed successfully.")


app = FastAPI(
    title="AI Knowledge Bot Backend",
    version="1.0.0",
    description="Backend API for Website & PDF RAG Chatbot",
    lifespan=lifespan
)

# Exception Handlers
app.add_exception_handler(AppBaseException, app_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Register Middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestTimeMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
setup_cors(app)

# Register API Routers
app.include_router(
    website.router,
    prefix="/api/v1",
    tags=["Website"]
)
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(
    chat.router,
    prefix="/api/v1",
    tags=["Chat"]
)
app.include_router(
    conversation.router,
    prefix="/api/v1",
    tags=["Conversation"]
)
app.include_router(
    sources.router,
    prefix="/api/v1",
    tags=["Sources"]
)
app.include_router(
    pdf.router,
    prefix="/api/v1",
    tags=["PDF"]
)


@app.get("/")
async def root():
    return {
        "message": "AI Knowledge Bot Backend is running."
    }