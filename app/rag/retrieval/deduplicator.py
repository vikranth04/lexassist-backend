import hashlib
from typing import List, Dict, Any
from app.core.logger import logger


class Deduplicator:
    """
    Prevents duplicate information from being included in the context.

    Responsibilities:
    - Detect duplicates using Chunk ID, Content hash, Source ID + Metadata
    - Merge duplicate context where appropriate
    """

    def deduplicate(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filters duplicate chunks from the list.
        """
        if not chunks:
            return []

        seen_ids = set()
        seen_hashes = set()
        unique_chunks = []

        logger.info(f"Deduplicating {len(chunks)} chunks.")

        for chunk in chunks:
            chunk_id = chunk.get("chunk_id")
            content = chunk.get("content", "")

            # 1. Check by ID
            if chunk_id and chunk_id in seen_ids:
                continue

            # 2. Check by Content Hash
            content_hash = self._generate_hash(content)
            if content_hash in seen_hashes:
                # If IDs are different but content is identical, it's a duplicate
                continue

            # If we reached here, it's unique
            if chunk_id:
                seen_ids.add(chunk_id)
            seen_hashes.add(content_hash)
            unique_chunks.append(chunk)

        logger.info(f"Remaining chunks after deduplication: {len(unique_chunks)}")
        return unique_chunks

    def _generate_hash(self, text: str) -> str:
        """Generates a SHA-256 hash of the normalized text content."""
        # Normalize text slightly for hashing (remove extra whitespace)
        normalized_text = " ".join(text.split()).lower()
        return hashlib.sha256(normalized_text.encode('utf-8')).hexdigest()
