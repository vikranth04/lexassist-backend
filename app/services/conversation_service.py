from app.repositories.conversation_repository import ConversationRepository
from typing import List, Dict, Any


class ConversationService:
    """
    Manages session lifecycles, message logs, and conversational history retrieval.
    """
    def __init__(self, repo: ConversationRepository):
        self.repo: ConversationRepository = repo

    def create_conversation(self) -> str:
        """Initializes a new chat conversation session."""
        return self.repo.create()

    def get_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Retrieves conversational history log for a session."""
        return self.repo.get_history(conversation_id)

    def delete_conversation(self, conversation_id: str) -> bool:
        """Removes a conversation session and all its logs."""
        return self.repo.delete(conversation_id)

    def add_message(self, conversation_id: str, role: str, content: str) -> bool:
        """Appends a new interaction message block to conversation logs."""
        return self.repo.add_message(conversation_id, role, content)
