from pydantic import BaseModel
from typing import List, Dict, Any


class ConversationCreateResponse(BaseModel):
    conversation_id: str
    success: bool


class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    history: List[Dict[str, Any]]


class ContinueRequest(BaseModel):
    question: str


class ContinueResponse(BaseModel):
    answer: str
    success: bool
