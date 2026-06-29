import time
from typing import List, Dict, Any
from app.embeddings.embedding_provider import EmbeddingProvider
from app.core.config import settings
from app.core.exceptions import BatchProcessingException
from app.core.logger import logger


class BatchProcessor:
    """
    Batches texts before sending requests to the embedding API, handling retry logic.
    """
    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider
        self.batch_size = settings.EMBEDDING_BATCH_SIZE
        self.retry_count = settings.EMBEDDING_RETRY_COUNT

    def process_batches(self, chunks: List[Dict[str, Any]]) -> List[List[float]]:
        """Processes chunks list in batches and returns list of vectors. Raises BatchProcessingException."""
        logger.info(f"Processing vector batches: {len(chunks)} chunks (Size: {self.batch_size})")
        all_vectors: List[List[float]] = []

        for offset in range(0, len(chunks), self.batch_size):
            batch = chunks[offset : offset + self.batch_size]
            texts = [c.get("content") or "" for c in batch]

            success = False
            vectors = []
            # Retry loop
            for attempt in range(self.retry_count):
                try:
                    vectors = self.provider.generate_embeddings(texts)
                    if len(vectors) == len(texts):
                        success = True
                        break
                except Exception as e:
                    logger.warning(f"Batch generation retry alert ({attempt+1}/{self.retry_count}): {str(e)}")
                    time.sleep(2 ** attempt)  # Exponential backoff

            if not success:
                raise BatchProcessingException("Failed to generate vector embeddings: retry limit exceeded.")

            all_vectors.extend(vectors)

        return all_vectors
