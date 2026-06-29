from typing import List, Dict, Any, Optional
from app.repositories.conversation_repository import ConversationRepository
from app.rag.pipeline.memory_manager import MemoryManager
from app.core.logger import logger

class ConversationManager:
    """
    Manages conversation lifecycle and connects memory to persistence.
    """

    def __init__(self, repository: Optional[ConversationRepository] = None):
        self.repository = repository or ConversationRepository()

    def get_or_create_conversation(self, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """Retrieves an existing conversation or starts a new one."""
        if conversation_id:
            history = self.repository.get_history(conversation_id)
            if history is not None:
                return {
                    "id": conversation_id,
                    "history": history
                }

        new_id = self.repository.create()
        logger.info(f"Created new conversation: {new_id}")
        return {
            "id": new_id,
            "history": []
        }

    def add_turn(self, conversation_id: str, question: str, answer: str):
        """Saves a single turn to the conversation history."""
        self.repository.add_message(conversation_id, "user", question)
        self.repository.add_message(conversation_id, "assistant", answer)
        logger.info(f"Updated conversation {conversation_id} with new turn.")

    def delete_conversation(self, conversation_id: str) -> bool:
        """Removes a conversation from storage."""
        return self.repository.delete(conversation_id)

    def get_memory(self, conversation_id: str) -> MemoryManager:
        """Returns a MemoryManager instance for the given conversation."""
        history = self.repository.get_history(conversation_id)
        return MemoryManager(history=history)
