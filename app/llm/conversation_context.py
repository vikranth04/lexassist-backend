from typing import List, Dict, Any, Optional

class ConversationContext:
    """
    Manages the short-term conversation memory for the LLM.
    """

    def __init__(self, history: Optional[List[Dict[str, str]]] = None):
        # history is expected to be a list of {"role": "user/assistant", "content": "..."}
        self.history = history or []

    def format_history(self, limit: int = 5) -> str:
        """
        Formats the last N messages into a string for the prompt.
        """
        if not self.history:
            return "No previous conversation history."

        recent_history = self.history[-limit:]
        formatted_parts = []

        for msg in recent_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted_parts.append(f"{role}: {msg['content']}")

        return "\n".join(formatted_parts)

    def add_message(self, role: str, content: str):
        """Adds a message to the history."""
        self.history.append({"role": role, "content": content})

    def get_last_user_query(self) -> Optional[str]:
        """Returns the last question asked by the user."""
        for msg in reversed(self.history):
            if msg["role"] == "user":
                return msg["content"]
        return None
