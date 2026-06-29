from typing import List, Dict, Any
from app.vectorstore.vector_manager import VectorManager
from app.vectorstore.vector_indexer import VectorIndexer
from app.vectorstore.collection_manager import CollectionManager
from app.core.config import settings


class VectorRepository:
    """
    Communicates directly with ChromaDB via indexing, validator, and management components.
    """
    def __init__(self, collection_name: str = None):
        active_col = collection_name or settings.VECTOR_COLLECTION_NAME
        self.manager = VectorManager(collection_name=active_col)
        self.indexer = VectorIndexer(collection_name=active_col)
        self.collection_manager = CollectionManager()
        self.collection_name = active_col

    def save_vectors(self, embedded_chunks: List[Dict[str, Any]]) -> int:
        """Indexes batch vectors using the VectorIndexer pipeline."""
        return self.indexer.index_embeddings(embedded_chunks)

    def delete_vectors(self, ids: List[str]):
        """Deletes vector documents by ID list."""
        self.manager.delete(ids)

    def retrieve_by_source(self, source_id: str) -> Dict[str, Any]:
        """Filters vector documents matching source ID parameter."""
        return self.manager.get_by_source(source_id)

    def get_collection_statistics(self) -> Dict[str, Any]:
        """Retrieves collection statistics."""
        return self.collection_manager.get_collection_stats(self.collection_name)

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Queries nearest neighbors matching the embedding vector.
        """

        # Convert empty filters {} to None
        if not filters:
            filters = None

        return self.manager.query(
            query_embeddings=[query_embedding],
            top_k=top_k,
            where=filters
        )
    def get_all_documents(self) -> Dict[str, Any]:
        """Retrieves all documents stored inside the collection."""
        try:
            return self.manager.collection.get()
        except Exception:
            return {"ids": [], "metadatas": [], "documents": []}
