import chromadb
from app.vectorstore.chroma_client import ChromaClient
from app.core.exceptions import CollectionException
from app.core.logger import logger
from typing import List, Dict, Any


class CollectionManager:
    """
    Manages vector database collections creation, deletion, and property statistics.
    """
    def __init__(self):
        self.chroma_client = ChromaClient().get_client()

    def get_or_create_collection(self, name: str) -> chromadb.Collection:
        """Loads or instantiates a ChromaDB collection. Raises CollectionException."""
        try:
            logger.info(f"Accessing/Creating collection: {name}")
            return self.chroma_client.get_or_create_collection(name)
        except Exception as e:
            raise CollectionException(f"Failed to resolve collection '{name}': {str(e)}")

    def delete_collection(self, name: str):
        """Deletes a collection by name. Raises CollectionException."""
        try:
            logger.info(f"Removing collection: {name}")
            self.chroma_client.delete_collection(name)
        except Exception as e:
            raise CollectionException(f"Failed to drop collection '{name}': {str(e)}")

    def list_collections(self) -> List[str]:
        """Lists active collections names."""
        try:
            collections = self.chroma_client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            raise CollectionException(f"Failed listing collections: {str(e)}")

    def get_collection_stats(self, name: str) -> Dict[str, Any]:
        """Retrieves collection document counts and parameters."""
        try:
            collection = self.get_or_create_collection(name)
            return {
                "name": name,
                "count": collection.count(),
                "metadata": collection.metadata or {}
            }
        except Exception as e:
            raise CollectionException(f"Collection stats query failed: {str(e)}")
