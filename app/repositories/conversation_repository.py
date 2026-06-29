import uuid
from typing import Dict, List, Any


class ConversationRepository:
    def __init__(self):
        # Thread-safe in-memory store for development/testing
        self._conversations: Dict[str, List[Dict[str, Any]]] = {}

    def create(self) -> str:
        conversation_id = str(uuid.uuid4())
        self._conversations[conversation_id] = []
        return conversation_id

    def get_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        return self._conversations.get(conversation_id, [])

    def delete(self, conversation_id: str) -> bool:
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            return True
        return False

    def add_message(self, conversation_id: str, role: str, content: str) -> bool:
        if conversation_id not in self._conversations:
            return False
        self._conversations[conversation_id].append({
            "role": role,
            "content": content
        })
        return True
