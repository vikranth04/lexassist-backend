from typing import List, Dict, Any
from app.rag.retrieval.context_builder import ContextBuilder
from app.core.logger import logger

class ContextManager:
    """
    Coordinates and merges context from multiple retrieval sources.

    Responsibilities:
    - Merge context chunks
    - Remove duplicates (delegated to deduplicator)
    - Handle token limits across different source types
    """

    def __init__(self):
        self.builder = ContextBuilder()

    def merge_and_format(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Synthesizes a cohesive context block from retrieved chunks.
        """
        logger.info(f"Merging {len(chunks)} context chunks.")
        return self.builder.build_context(chunks)
