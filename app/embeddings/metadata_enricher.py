import time
from typing import Dict, Any
from app.core.config import settings


class MetadataEnricher:
    """
    Attaches model names, dimensions, timestamps, and lineage IDs to chunk metadata.
    """
    def enrich(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        """Combines original chunk indices and source tracking attributes with embedding details."""
        original_meta = chunk.get("metadata") or {}

        return {
            "source_id": original_meta.get("source_id"),
            "document_id": original_meta.get("parent_document_id"),
            "chunk_id": chunk.get("chunk_id"),
            "location": original_meta.get("location", {}),
            "statistics": original_meta.get("statistics", {}),
            "source_information": original_meta.get("source_information", {}),
            "embedding_model": settings.EMBEDDING_MODEL,
            "embedding_version": "1.0.0",
            "generated_at": float(time.time())
        }
