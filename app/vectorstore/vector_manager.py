from typing import List, Dict, Any
from app.vectorstore.collection_manager import CollectionManager
from app.core.exceptions import VectorStoreException


class VectorManager:
    """
    Manages vector operations (Insert, Update, Delete, Upsert, Query) on a target ChromaDB collection.
    """
    def __init__(self, collection_name: str = "knowledge_base"):
        self.collection_manager = CollectionManager()
        self.collection = self.collection_manager.get_or_create_collection(collection_name)

    def insert(self, ids: List[str], documents: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]]):
        """Inserts vector records. Raises VectorStoreException."""
        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
        except Exception as e:
            raise VectorStoreException(f"Failed inserting vectors into ChromaDB: {str(e)}")

    def update(self, ids: List[str], documents: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]]):
        """Updates vector records. Raises VectorStoreException."""
        try:
            self.collection.update(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
        except Exception as e:
            raise VectorStoreException(f"Failed updating vectors in ChromaDB: {str(e)}")

    def upsert(self, ids: List[str], documents: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]]):
        """Upserts vector records. Raises VectorStoreException."""
        try:
            self.collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
        except Exception as e:
            raise VectorStoreException(f"Failed upserting vectors in ChromaDB: {str(e)}")

    def delete(self, ids: List[str]):
        """Deletes vector records by ID list. Raises VectorStoreException."""
        try:
            self.collection.delete(ids=ids)
        except Exception as e:
            raise VectorStoreException(f"Failed deleting vectors from ChromaDB: {str(e)}")

    def get_by_ids(self, ids: List[str]) -> Dict[str, Any]:
        """Retrieves document records by ID list."""
        try:
            return self.collection.get(ids=ids)
        except Exception as e:
            raise VectorStoreException(f"Failed retrieving vectors by IDs from ChromaDB: {str(e)}")

    def get_by_source(self, source_id: str) -> Dict[str, Any]:
        """Retrieves document records matching source ID filter."""
        try:
            return self.collection.get(where={"source_id": source_id})
        except Exception as e:
            raise VectorStoreException(f"Failed filtering vectors by source ID: {str(e)}")

    def query(
        self,
        query_embeddings: List[List[float]],
        top_k: int = 5,
        where: Dict[str, Any] = None
    ):
        """Executes nearest-neighbor query search."""
        try:
            query_args = {
                "query_embeddings": query_embeddings,
                "n_results": top_k,
            }

            # Only pass the where parameter when filters actually exist
            if where is not None:
                query_args["where"] = where

            return self.collection.query(**query_args)

        except Exception as e:
            raise VectorStoreException(
                f"Failed querying vectors from ChromaDB: {str(e)}"
            )