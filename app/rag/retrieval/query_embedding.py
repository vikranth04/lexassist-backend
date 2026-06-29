from typing import List, Dict, Any, Optional
from app.embeddings.embedding_factory import EmbeddingFactory
from app.core.exceptions import EmbeddingGenerationException, EmbeddingValidationException
from app.core.logger import logger


class QueryEmbedding:
    """
    Generates embedding vectors for user queries.

    Responsibilities:
    - Use the configured embedding provider
    - Generate semantic query vectors
    - Validate generated embeddings
    - Attach request metadata
    - Support batching for future expansion
    """
    def __init__(self):
        self.provider = EmbeddingFactory().get_provider()

    def embed_query(self, query: str, metadata: Optional[Dict[str, Any]] = None) -> List[float]:
        """
        Encodes query string into a vector using RETRIEVAL_QUERY task type.
        """
        try:
            logger.info(f"Generating embedding for query. Metadata: {metadata}")
            # Use RETRIEVAL_QUERY for optimized search performance and correct model mapping
            vectors = self.provider.generate_embeddings([query], task_type="RETRIEVAL_QUERY")

            if not vectors or len(vectors) == 0:
                raise EmbeddingGenerationException("Provider generated an empty vector list.")

            vector = vectors[0]
            self._validate_embedding(vector)

            return vector
        except (EmbeddingGenerationException, EmbeddingValidationException):
            raise
        except Exception as e:
            logger.error(f"Unexpected error during query embedding: {str(e)}")
            raise EmbeddingGenerationException(f"Query vector generation failed: {str(e)}")

    def embed_queries(self, queries: List[str]) -> List[List[float]]:
        """
        Supports batch embedding of queries.
        """
        try:
            vectors = self.provider.generate_embeddings(queries, task_type="RETRIEVAL_QUERY")
            for v in vectors:
                self._validate_embedding(v)
            return vectors
        except Exception as e:
            raise EmbeddingGenerationException(f"Batch query embedding failed: {str(e)}")

    def _validate_embedding(self, vector: List[float]):
        """Validates the generated embedding vector (768 dims)."""
        if not vector:
            raise EmbeddingValidationException("Generated vector is empty.")

        if len(vector) != 768:
            logger.warning(f"Unexpected embedding dimension: {len(vector)} (expected 768)")

        if any(x != x for x in vector): # NaN check
             raise EmbeddingValidationException("Generated vector contains NaN values.")


class MockQueryEmbedding(QueryEmbedding):
    """
    Mock class for testing environments.
    """
    def embed_query(self, query: str, metadata: Optional[Dict[str, Any]] = None) -> List[float]:
        return [0.1] * 768

    def embed_queries(self, queries: List[str]) -> List[List[float]]:
        return [[0.1] * 768 for _ in queries]
