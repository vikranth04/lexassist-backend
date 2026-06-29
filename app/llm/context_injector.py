from typing import List, Dict, Any
from app.rag.retrieval.context_builder import ContextBuilder
from app.core.logger import logger

class ContextInjector:
    """
    Responsible for injecting retrieved context into the prompt preparation flow.
    Wraps the RAG ContextBuilder for LLM-specific needs.
    """

    def __init__(self):
        self.builder = ContextBuilder()

    def prepare_context(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Processes chunks into a context string suitable for the LLM prompt.
        """
        logger.info("Injecting context into LLM flow.")
        return self.builder.build_context(chunks)
