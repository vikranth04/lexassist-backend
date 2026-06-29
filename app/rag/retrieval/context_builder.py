from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.exceptions import ContextBuilderException
from app.core.logger import logger


class ContextBuilder:
    """
    Builds the final context string for the LLM.

    Responsibilities:
    - Merge retrieved chunks
    - Preserve logical order
    - Respect token limits
    - Maintain section boundaries and references
    """

    def __init__(self):
        self.max_tokens = getattr(settings, "RAG_MAX_CONTEXT_TOKENS", 4000)
        # 1 token approx 4 characters
        self.max_chars = self.max_tokens * 4

    def build_context(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Assembles chunks into a single formatted context string.
        """
        if not chunks:
            return "No relevant context found."

        try:
            logger.info(f"Building context from {len(chunks)} chunks.")

            # Sort chunks by source and page/index to maintain logical flow
            # (If that metadata is available)
            sorted_chunks = self._sort_chunks_for_context(chunks)

            context_parts = []
            current_length = 0

            for i, chunk in enumerate(sorted_chunks):
                chunk_text = self._format_chunk(chunk, i + 1)

                if current_length + len(chunk_text) > self.max_chars:
                    logger.warning(f"Context limit reached. Skipping remaining chunks.")
                    break

                context_parts.append(chunk_text)
                current_length += len(chunk_text)

            return "\n\n---\n\n".join(context_parts)

        except Exception as e:
            logger.error(f"Context building failure: {str(e)}")
            raise ContextBuilderException(f"Context synthesis step failed: {str(e)}")

    def _sort_chunks_for_context(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sorts chunks to preserve document hierarchy and logical order."""
        # Primary sort: source_id, Secondary sort: page_number or chunk_index
        def sort_key(c):
            meta = c.get("metadata", {})
            return (
                str(meta.get("source_id", "")),
                int(meta.get("page_number", 0)),
                int(meta.get("chunk_index", 0))
            )

        return sorted(chunks, key=sort_key)

    def _format_chunk(self, chunk: Dict[str, Any], index: int) -> str:
        """Formats an individual chunk for inclusion in the context."""
        content = chunk.get("content", "")
        metadata = chunk.get("metadata", {})

        source_info = self._get_source_label(metadata)

        return f"[Source {index}: {source_info}]\n{content}"

    def _get_source_label(self, metadata: Dict[str, Any]) -> str:
        """Extracts a human-readable source label from metadata."""
        if "website_url" in metadata:
            return f"URL: {metadata['website_url']}"
        elif "pdf_filename" in metadata:
            page = metadata.get("page_number", "unknown")
            return f"PDF: {metadata['pdf_filename']} (Page {page})"
        elif "source_id" in metadata:
            return f"Source ID: {metadata['source_id']}"
        return "Unknown Source"
