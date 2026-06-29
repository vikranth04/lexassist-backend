from typing import List, Dict, Any
from app.vectorstore.vector_manager import VectorManager
from app.vectorstore.vector_validator import VectorValidator
from app.vectorstore.metadata_manager import MetadataManager
from app.core.exceptions import IndexingException
from app.core.logger import logger
from app.core.config import settings


class VectorIndexer:
    """
    Handles index formatting, validation, and batch write insertions.
    """
    def __init__(self, collection_name: str = None):
        active_col = collection_name or settings.VECTOR_COLLECTION_NAME
        self.manager = VectorManager(collection_name=active_col)
        self.validator = VectorValidator()
        self.metadata_manager = MetadataManager()
        self.batch_size = settings.VECTOR_BATCH_SIZE

    def index_embeddings(self, embedded_chunks: List[Dict[str, Any]]) -> int:
        """Validates and indexes chunks list. Returns count of indexed records. Raises IndexingException."""
        if not embedded_chunks:
            return 0

        logger.info(f"Starting batch vector indexing of {len(embedded_chunks)} items.")

        # 1. Pre-validation checks
        for item in embedded_chunks:
            self.validator.validate_vector(
                item.get("chunk_id") or "",
                item.get("embedding") or [],
                item.get("metadata") or {}
            )

        indexed_count = 0
        # 2. Batch ingestion
        for offset in range(0, len(embedded_chunks), self.batch_size):
            batch = embedded_chunks[offset : offset + self.batch_size]

            ids = [ch.get("chunk_id") or "" for ch in batch]
            documents = [ch.get("content") or "" for ch in batch]
            embeddings = [ch.get("embedding") or [] for ch in batch]
            metadatas = [self.metadata_manager.sanitize_metadata(ch.get("metadata") or {}) for ch in batch]

            try:
                # Use upsert to overwrite duplicates cleanly
                self.manager.upsert(ids, documents, embeddings, metadatas)
                indexed_count += len(batch)
            except Exception as e:
                raise IndexingException(f"Batch vector insertion offset {offset} failed: {str(e)}")

        logger.info(f"Indexing completed successfully. Count: {indexed_count}")
        return indexed_count
