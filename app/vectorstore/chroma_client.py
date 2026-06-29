import chromadb
from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import VectorStoreException


class ChromaClient:
    """
    Singleton connection manager for the ChromaDB vector database.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaClient, cls).__new__(cls)
            try:
                logger.info(f"Initializing persistent ChromaDB client path: {settings.CHROMA_DB_PATH}")
                cls._instance.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
            except Exception as e:
                raise VectorStoreException(f"ChromaDB persistent client initialization failed: {str(e)}")
        return cls._instance

    def get_client(self) -> chromadb.PersistentClient:
        """Returns the active persistent client connection."""
        return self.client
