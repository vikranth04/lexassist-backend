from app.vectorstore.collection_manager import CollectionManager
from app.vectorstore.chroma_client import ChromaClient
from typing import Dict, Any


class VectorHealth:
    """
    Evaluates ChromaDB connection status, collection metrics, and persistent storage details.
    """
    def __init__(self):
        self.collection_manager = CollectionManager()
        self.chroma_client = ChromaClient().get_client()

    def check_health(self) -> Dict[str, Any]:
        """Runs health diagnostics and returns metrics dictionary."""
        try:
            collections = self.collection_manager.list_collections()
            total_vectors = 0

            for col in collections:
                stats = self.collection_manager.get_collection_stats(col)
                total_vectors += stats.get("count", 0)

            # Retrieve database path config value safely
            db_dir = "unknown"
            if hasattr(self.chroma_client, "_settings"):
                try:
                    db_dir = getattr(self.chroma_client._settings, "persist_directory", "unknown")
                except Exception:
                    pass

            return {
                "status": "healthy",
                "collections_count": len(collections),
                "collections_list": collections,
                "total_vectors_count": total_vectors,
                "database_directory": str(db_dir)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
