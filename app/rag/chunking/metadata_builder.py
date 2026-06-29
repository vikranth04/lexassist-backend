import time
from typing import Dict, Any


class MetadataBuilder:
    """
    Builds rich location, statistics, and lineage attribution parameters for chunk files.
    """
    def build_metadata(
        self,
        chunk_id: str,
        chunk_index: int,
        doc: Dict[str, Any],
        chunk_text: str,
        char_count: int,
        token_count: int
    ) -> Dict[str, Any]:
        """Assembles the metadata dictionary mapping for a specific text chunk."""
        words_count = len(chunk_text.split())

        return {
            "chunk_id": chunk_id,
            "chunk_index": chunk_index,
            "parent_document_id": doc.get("document_id", "unknown"),
            "source_id": doc.get("source_id", "unknown"),
            "source_type": doc.get("source_type", "WEBSITE"),
            "location": {
                "page_number": 1,  # PDF page details can be mapped here
                "section_name": "Body",
                "heading": doc.get("title", ""),
                "subheading": ""
            },
            "statistics": {
                "character_count": char_count,
                "token_count": token_count,
                "word_count": words_count
            },
            "source_information": {
                "original_filename_url": doc.get("original_filename_url", ""),
                "document_title": doc.get("title", "")
            },
            "processing": {
                "chunk_version": "1.0.0",
                "processing_timestamp": float(time.time())
            }
        }
