from abc import ABC, abstractmethod
from typing import List, Optional
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.exceptions import EmbeddingProviderException
from app.core.logger import logger


class EmbeddingProvider(ABC):
    """
    Abstract interface for vector embedding generation engines.
    """
    @abstractmethod
    def generate_embeddings(self, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
        """Generates embedding vectors for the list of texts."""
        pass


class GeminiEmbeddingProvider(EmbeddingProvider):
    """
    Uses Google GenAI SDK to generate high-dimensional vectors.
    """
    def __init__(self):
        try:
            # Force API version to 'v1' to avoid 'v1beta' 404 errors for gemini-embedding-001
            self.client = genai.Client(
                api_key=settings.GEMINI_API_KEY,
                http_options={'api_version': 'v1'}
            )

            self.model = settings.EMBEDDING_MODEL
            logger.info(f"Initialized GeminiEmbeddingProvider with model: {self.model} (API: v1)")
        except Exception as e:
            raise EmbeddingProviderException(f"Failed to initialize Gemini API client: {str(e)}")

    def generate_embeddings(self, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
        """
        Generates embeddings for the list of texts.
        Uses task_type for model optimization (RETRIEVAL_DOCUMENT or RETRIEVAL_QUERY).
        """
        if not texts:
            return []

        try:
            # We use the config to specify task_type which is recommended for gemini-embedding-001.
            # This can help the API correctly route the request and avoid 404 mapping errors.
            config = types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=768  # gemini-embedding-001 standard
            )

            response = self.client.models.embed_content(
                model=self.model,
                contents=texts,
                config=config
            )

            if not response or not response.embeddings:
                raise EmbeddingProviderException("Gemini API returned an empty embedding response.")

            return [emb.values for emb in response.embeddings]
        except Exception as e:
            # Detailed error logging to identify 404 or unsupported operations
            logger.error(f"Gemini embedding API failure: {str(e)}")
            raise EmbeddingProviderException(f"Gemini embedding API call failed: {str(e)}")


class MockEmbeddingProvider(EmbeddingProvider):
    """
    Mock provider for fallback/testing environments.
    """
    def generate_embeddings(self, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
        # text-embedding-004 has 768 dimensions.
        return [[0.1] * 768 for _ in texts]
