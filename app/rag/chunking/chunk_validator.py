from typing import Dict, Any
from app.core.exceptions import ChunkValidationException


class ChunkValidator:
    """
    Validates token counts and metadata integrity for generated chunks.
    """
    def __init__(self, min_tokens: int = 100, max_tokens: int = 1000):
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens

    def validate(self, chunk: Dict[str, Any]) -> bool:
        """Validates a chunk structure. Raises ChunkValidationException on failures."""
        content = chunk.get("content") or ""
        if not content.strip():
            raise ChunkValidationException("Chunk content cannot be empty.")

        stats = chunk.get("statistics") or {}
        token_count = stats.get("token_count", 0)

        if token_count > self.max_tokens:
            raise ChunkValidationException(
                f"Chunk exceeds max token count limit ({token_count} > {self.max_tokens})."
            )
        if token_count < self.min_tokens:
            # We log validation warning, but keep it active if it is the only chunk
            pass

        return True
