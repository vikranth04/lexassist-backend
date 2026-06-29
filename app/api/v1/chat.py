from fastapi import APIRouter, Depends
import anyio
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.core.dependencies import get_chat_service
from app.core.exceptions import AppBaseException

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with Legal Knowledge Base",
    description="Submits a query to the legal AI RAG pipeline to generate context-grounded answers."
)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        response = await chat_service.chat(
            question=request.question,
            conversation_id=request.conversation_id if hasattr(request, 'conversation_id') else None
        )
        return response
    except Exception as e:
        raise AppBaseException(message=str(e), status_code=500)
