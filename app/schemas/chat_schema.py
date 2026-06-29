from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None

class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class RetrievalInfo(BaseModel):
    chunks_found: int
    sources_used: int

class ChatResponse(BaseModel):
    success: bool
    conversation_id: str
    answer: str
    citations: List[Dict[str, Any]] = []
    processing_time_ms: int
    token_usage: Optional[TokenUsage] = None
    retrieval: Optional[RetrievalInfo] = None
    metadata: Optional[Dict[str, Any]] = None
