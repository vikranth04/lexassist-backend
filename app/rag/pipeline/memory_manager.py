from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logger import logger

class MemoryManager:
    """
    Manages short-term conversation memory and context window.

    Responsibilities:
    - Maintain message history
    - Summarize older context (future expansion)
    - Identify active topic
    """

    def __init__(self, history: Optional[List[Dict[str, Any]]] = None):
        self.history = history or []
        self.max_messages = getattr(settings, "MAX_CONVERSATION_HISTORY", 10)

    def get_recent_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Returns the most recent N messages."""
        k = limit or self.max_messages
        return self.history[-k:]

    def get_context_summary(self) -> str:
        """
        Heuristic-based topic or summary extraction.
        For now, returns a simple combined string of recent turns.
        """
        recent = self.get_recent_history(limit=3)
        summary_parts = []
        for msg in recent:
            role = msg.get("role", "unknown").capitalize()
            content = msg.get("content", "")[:100] + "..."
            summary_parts.append(f"{role}: {content}")
        return " | ".join(summary_parts)

    def extract_intent_context(self) -> Dict[str, Any]:
        """Identifies active topic or intent from memory."""
        # Future: Use NLP to extract topic
        return {
            "last_topic": None,
            "turn_count": len(self.history)
        }

    def format_history(self) -> List[Dict[str, str]]:
        """
        Formats conversation history for the Gemini API.
        """
        formatted = []

        for msg in self.get_recent_history():
            formatted.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        return formatted
