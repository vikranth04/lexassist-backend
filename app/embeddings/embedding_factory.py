from app.embeddings.embedding_provider import EmbeddingProvider, GeminiEmbeddingProvider, MockEmbeddingProvider
from app.core.config import settings
from app.core.exceptions import EmbeddingProviderException


class EmbeddingFactory:
    """
    Selects and instantiates the configured vector embedding provider.
    """
    def get_provider(self) -> EmbeddingProvider:
        """Returns the active EmbeddingProvider instance."""
        provider_name = settings.EMBEDDING_PROVIDER.lower()
        if provider_name == "gemini":
            return GeminiEmbeddingProvider()
        elif provider_name == "mock":
            return MockEmbeddingProvider()
        else:
            raise EmbeddingProviderException(
                f"Unsupported embedding provider name configured: '{settings.EMBEDDING_PROVIDER}'"
            )
