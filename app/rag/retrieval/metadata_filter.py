from typing import List, Dict, Any, Optional
from app.core.exceptions import MetadataFilterException
from app.core.logger import logger


class MetadataFilter:
    """
    Implements intelligent filtering for retrieved chunks.

    Responsibilities:
    - Support various filter types (source_type, url, filename, etc.)
    - Extensible filtering logic
    """

    SUPPORTED_FILTERS = [
        "source_type", "website_url", "pdf_filename", "page_number",
        "document_id", "source_id", "collection", "date", "processing_status"
    ]

    def filter_results(self, chunks: List[Dict[str, Any]], filters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Applies filters to the chunks.
        In many cases, this is handled at the database level, but this module
        can perform additional filtering or validation.
        """
        if not filters:
            return chunks

        try:
            logger.info(f"Applying metadata filters: {filters}")
            filtered = []
            for chunk in chunks:
                metadata = chunk.get("metadata") or {}
                if self._matches_filters(metadata, filters):
                    filtered.append(chunk)

            return filtered
        except Exception as e:
            logger.error(f"Metadata filtering error: {str(e)}")
            raise MetadataFilterException(f"Failed to execute metadata filtering: {str(e)}")

    def _matches_filters(self, metadata: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Checks if metadata matches all provided filters."""
        for key, expected_val in filters.items():
            if key not in self.SUPPORTED_FILTERS:
                logger.warning(f"Filter key '{key}' is not explicitly supported, but applying anyway.")

            actual_val = metadata.get(key)

            # Support basic equality. Can be expanded for ranges, list inclusion, etc.
            if isinstance(expected_val, list):
                if actual_val not in expected_val:
                    return False
            elif actual_val != expected_val:
                return False

        return True

    def build_chroma_filter(
        self,
        filters: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Converts generic filters into a valid ChromaDB 'where' clause.
        Returns None when no filters are supplied.
        """

        # IMPORTANT:
        # ChromaDB does NOT accept where={}
        if not filters:
            return None

        if len(filters) == 1:
            return filters

        return {
            "$and": [
                {key: value}
                for key, value in filters.items()
            ]
        }
