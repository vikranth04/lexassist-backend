from fastapi import APIRouter, Depends
import anyio
from app.core.dependencies import get_conversation_service, get_chat_service
from app.services.conversation_service import ConversationService
from app.services.chat_service import ChatService
from app.schemas.conversation_schema import (
    ConversationCreateResponse,
    ConversationHistoryResponse,
    ContinueRequest,
    ContinueResponse
)
from app.core.exceptions import EntityNotFoundException

router = APIRouter()


@router.post(
    "/conversations",
    response_model=ConversationCreateResponse,
    summary="Create Conversation Session",
    description="Initializes a new legal advice chat session."
)
async def create_conversation(
    service: ConversationService = Depends(get_conversation_service)
):
    conv_id = service.create_conversation()
    return {"conversation_id": conv_id, "success": True}


@router.get(
    "/conversations/{id}",
    response_model=ConversationHistoryResponse,
    summary="Get Conversation History",
    description="Retrieves message logs recorded for a conversation session."
)
async def get_conversation(
    id: str,
    service: ConversationService = Depends(get_conversation_service)
):
    history = service.get_history(id)
    return {"conversation_id": id, "history": history}


@router.delete(
    "/conversations/{id}",
    summary="Delete Conversation Session",
    description="Deletes all conversation log details."
)
async def delete_conversation(
    id: str,
    service: ConversationService = Depends(get_conversation_service)
):
    deleted = service.delete_conversation(id)
    if not deleted:
        raise EntityNotFoundException("Conversation not found")
    return {"success": True}


@router.post(
    "/conversations/{id}/continue",
    response_model=ContinueResponse,
    summary="Continue Conversation Session",
    description="Submits a query within an existing session and logs the response history."
)
async def continue_conversation(
    id: str,
    request: ContinueRequest,
    conv_service: ConversationService = Depends(get_conversation_service),
    chat_service: ChatService = Depends(get_chat_service)
):
    # Try adding user message
    if not conv_service.add_message(id, "user", request.question):
        raise EntityNotFoundException("Conversation not found")

    # Generate answer inside threadpool
    result = await anyio.to_thread.run_sync(chat_service.chat, request.question)
    answer = result.get("answer", "")

    # Save assistant message
    conv_service.add_message(id, "assistant", answer)

    return {"answer": answer, "success": True}
