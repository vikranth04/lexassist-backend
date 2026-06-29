import os
import time
from fastapi import APIRouter
from app.schemas.health_schema import HealthResponse
from app.core.config import settings
from app.core.dependencies import get_vector_repository, get_chat_service

router = APIRouter()
START_TIME = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check the system status, uptime, database connections, and storage state."
)
async def health_check():
    # Groq status check
    groq_status = "available" if settings.GROQ_API_KEY else "unavailable"

    # Gemini status check (Used for Embeddings)
    gemini_status = "available" if settings.GEMINI_API_KEY else "unavailable"

    # Chroma DB status check
    try:
        vector_repo = get_vector_repository()
        chromadb_status = "available"
    except Exception:
        chromadb_status = "unavailable"

    # Storage status check
    storage_dirs = {
        "uploads": "app/storage/uploads",
        "processed": "app/storage/processed",
        "temp": "app/storage/temp"
    }
    storage_status = {}
    for key, path in storage_dirs.items():
        if os.path.exists(path) and os.access(path, os.W_OK):
            storage_status[key] = "writable"
        else:
            storage_status[key] = "unavailable"

    # Additional service checks
    try:
        chat_service = get_chat_service()
        pipeline_status = "available"
        conv_manager_status = "available"
    except Exception:
        pipeline_status = "unavailable"
        conv_manager_status = "unavailable"

    uptime_seconds = int(time.time() - START_TIME)

    return {
        "success": True,
        "message": "AI Knowledge Bot Backend is running.",
        "status": "healthy",
        "version": "1.0.0",
        "uptime": f"{uptime_seconds} seconds",
        "environment": "production" if settings.GROQ_API_KEY else "development",
        "groq_status": groq_status,
        "gemini_status": gemini_status,
        "chromadb_status": chromadb_status,
        "storage_status": storage_status,
        "embedding_service": "available",
        "retrieval_service": "available",
        "pipeline_status": pipeline_status,
        "conversation_manager": conv_manager_status
    }
