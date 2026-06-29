import os
import time
import fitz
from typing import Dict, Any


class MetadataExtractor:
    """
    Safely extracts PDF document attributes (author, creator, pages count, timestamps).
    """
    def extract(self, doc: fitz.Document, file_path: str, source_id: str) -> Dict[str, Any]:
        """Extracts metadata fields from a fitz.Document."""
        meta = doc.metadata or {}
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

        # Retrieve PDF Version string safely
        version_str = "unknown"
        if hasattr(doc, "pdf_version"):
            # fitz document version can be method or property
            try:
                version_str = doc.pdf_version() if callable(doc.pdf_version) else doc.pdf_version
            except Exception:
                pass

        return {
            "source_id": source_id,
            "filename": os.path.basename(file_path),
            "original_filename": os.path.basename(file_path),
            "file_size": file_size,
            "number_of_pages": len(doc),
            "pdf_version": str(version_str),
            "author": meta.get("author") or "",
            "creator": meta.get("creator") or "",
            "producer": meta.get("producer") or "",
            "creation_date": meta.get("creationDate") or "",
            "modified_date": meta.get("modDate") or "",
            "upload_timestamp": float(time.time())
        }
