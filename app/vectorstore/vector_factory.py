from app.vectorstore.vector_manager import VectorManager
from app.core.config import settings


class VectorFactory:
    """
    Instantiates VectorManager configurations for different collections.
    """
    def get_vector_manager(self, collection_name: str = None) -> VectorManager:
        """Returns a VectorManager instance configured for the specified collection."""
        active_col = collection_name or settings.VECTOR_COLLECTION_NAME
        return VectorManager(collection_name=active_col)
