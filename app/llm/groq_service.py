import time
from typing import Optional, List, Dict, Generator
from groq import Groq

from app.core.config import settings
from app.core.exceptions import (
    GroqConnectionException,
    EmbeddingProviderException,
)
from app.core.logger import logger
from app.embeddings.embedding_factory import EmbeddingFactory


class GroqService:
    """
    Centralized service for interacting with the Groq API.
    """

    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise GroqConnectionException("GROQ_API_KEY is not configured.")

        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model_id = settings.GROQ_MODEL

    async def generate_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Sends a request to Groq and returns the generated text.
        """
        try:
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})

            if history:
                for msg in history:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })

            messages.append({"role": "user", "content": prompt})

            logger.info(f"Groq request for model {self.model_id}")

            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model_id,
                temperature=getattr(settings, "LLM_TEMPERATURE", 0.2),
                max_tokens=getattr(settings, "LLM_MAX_OUTPUT_TOKENS", 1024),
                top_p=getattr(settings, "LLM_TOP_P", 0.95),
            )

            if chat_completion.choices:
                return chat_completion.choices[0].message.content

            return ""

        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise GroqConnectionException(f"Failed to connect to Groq: {e}")

    async def stream_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """
        Streams response from Groq.
        """
        try:
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})

            messages.append({"role": "user", "content": prompt})

            stream = self.client.chat.completions.create(
                messages=messages,
                model=self.model_id,
                temperature=getattr(settings, "LLM_TEMPERATURE", 0.2),
                max_tokens=getattr(settings, "LLM_MAX_OUTPUT_TOKENS", 1024),
                top_p=getattr(settings, "LLM_TOP_P", 0.95),
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"Groq streaming error: {e}")
            raise GroqConnectionException(f"Groq streaming failed: {e}")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generates embedding representation using the configured embedding provider.
        Note: Preserves existing Gemini embedding usage.
        """
        try:
            provider = EmbeddingFactory().get_provider()
            vectors = provider.generate_embeddings(
                [text],
                task_type="RETRIEVAL_QUERY",
            )

            if not vectors:
                raise GroqConnectionException("Generated empty embedding list.")

            return vectors[0]

        except (EmbeddingProviderException, Exception) as e:
            logger.error(f"Embedding generation error in GroqService: {e}")
            raise GroqConnectionException(f"Failed to generate embedding: {e}")
