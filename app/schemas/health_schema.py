from pydantic import BaseModel
from typing import Dict, Optional


class HealthResponse(BaseModel):
    success: bool
    message: str
    status: str
    version: str
    uptime: str
    environment: str
    groq_status: str
    gemini_status: str
    chromadb_status: str
    storage_status: Dict[str, str]
    embedding_service: str = "available"
    retrieval_service: str = "available"
    pipeline_status: str = "available"
    conversation_manager: str = "available"
