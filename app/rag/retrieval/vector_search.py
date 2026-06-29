from typing import List, Dict, Any, Optional
from app.repositories.vector_repository import VectorRepository
from app.core.config import settings
from app.core.exceptions import SimilaritySearchException
from app.core.logger import logger


class VectorSearch:
    """
    Retrieves candidate vectors matching the user query.

    Responsibilities:
    - Search ChromaDB
    - Top-K retrieval
    - Configurable similarity threshold
    - Metadata filtering
    - Source filtering
    - Collection selection
    - Batch retrieval
    """
    def __init__(self, collection_name: Optional[str] = None):
        self.collection_name = collection_name or settings.VECTOR_COLLECTION_NAME
        self.repository = VectorRepository(collection_name=self.collection_name)
        self.default_top_k = settings.RAG_TOP_K
        self.similarity_threshold = getattr(settings, "RAG_SIMILARITY_THRESHOLD", 0.0)

    def search_vectors(
        self,
        query_embedding: List[float],
        top_k: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Queries the vector repository.
        """
        k = top_k or self.default_top_k
        try:
            logger.info(f"Searching vectors in collection '{self.collection_name}' with top_k={k} and filters={filters}")
            results = self.repository.search(query_embedding, top_k=k, filters=filters)

            if not results or not results.get("ids"):
                return []

            ids = results.get("ids", [[]])[0]
            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0] if "distances" in results else [1.0] * len(ids)

            chunks = []
            for idx in range(len(ids)):
                # Convert distance to similarity score
                # ChromaDB often uses squared L2 distance, so 1.0 - distance is a heuristic.
                # If using cosine similarity, distance is 1.0 - similarity.
                similarity_score = float(1.0 - distances[idx])

                if similarity_score < self.similarity_threshold:
                    continue

                chunks.append({
                    "chunk_id": ids[idx],
                    "content": documents[idx],
                    "metadata": metadatas[idx],
                    "similarity_score": similarity_score,
                    "collection": self.collection_name
                })

            return chunks
        except Exception as e:
            logger.error(f"Vector search failure: {str(e)}")
            raise SimilaritySearchException(f"Vector similarity search failure: {str(e)}")

    def batch_search(
        self,
        query_embeddings: List[List[float]],
        top_k: Optional[int] = None
    ) -> List[List[Dict[str, Any]]]:
        """Supports batch retrieval for future expansion."""
        # This would require updating VectorRepository to support batch search if not already
        # For now, we can iterate, but real batching is better.
        results = []
        for emb in query_embeddings:
            results.append(self.search_vectors(emb, top_k=top_k))
        return results
