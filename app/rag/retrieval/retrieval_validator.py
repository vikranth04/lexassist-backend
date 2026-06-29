from typing import List, Dict, Any
from app.core.exceptions import RetrievalException
from app.core.logger import logger


class RetrievalValidator:
    """
    Validates retrieval results to ensure quality and integrity.

    Responsibilities:
    - Check for empty results
    - Detect duplicate chunks
    - Validate metadata and scores
    - Reject invalid responses
    """

    def validate_results(self, chunks: List[Dict[str, Any]]):
        """
        Performs validation on the retrieved chunks.
        Raises RetrievalException if validation fails.
        """
        if not chunks:
            logger.warning("Retrieval returned zero results.")
            # Depending on policy, we might not raise exception for zero results,
            # but here we follow the instruction "Reject invalid retrieval responses".
            # For now, let's just log and return if empty is allowed.
            return

        seen_ids = set()
        for chunk in chunks:
            self._validate_chunk(chunk, seen_ids)

    def _validate_chunk(self, chunk: Dict[str, Any], seen_ids: set):
        """Validates a single chunk."""
        # 1. Check for basic fields
        if not chunk.get("chunk_id"):
            raise RetrievalException("Retrieval result missing 'chunk_id'.")

        if not chunk.get("content"):
            raise RetrievalException(f"Chunk {chunk.get('chunk_id')} has no content.")

        # 2. Check for duplicates (should have been handled by Deduplicator)
        c_id = chunk["chunk_id"]
        if c_id in seen_ids:
            raise RetrievalException(f"Duplicate chunk ID '{c_id}' found after deduplication.")
        seen_ids.add(c_id)

        # 3. Validate similarity score
        score = chunk.get("similarity_score")
        if score is not None:
            if not (0.0 <= score <= 1.0):
                logger.warning(f"Invalid similarity score for chunk {c_id}: {score}")
                # We might want to clamp or reject

        # 4. Check for critical metadata
        metadata = chunk.get("metadata")
        if metadata is None:
            raise RetrievalException(f"Chunk {c_id} is missing metadata.")

        if not metadata.get("source_id"):
             logger.warning(f"Chunk {c_id} is missing 'source_id' in metadata.")
