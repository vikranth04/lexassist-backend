import uuid
import time
from typing import Dict, Any, List


class PDFFactory:
    """
    Standardizes page logs and document metadata outputs into standard document packages.
    """
    def create_document(self, source_id: str, metadata: Dict[str, Any], pages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Creates and returns the standardized PDF document representation dictionary."""
        doc_id = f"DOC_{uuid.uuid4().hex[:8].upper()}"

        return {
            "source_id": source_id,
            "document_id": doc_id,
            "metadata": metadata,
            "total_pages": len(pages),
            "processing_timestamp": float(time.time()),
            "pages": pages
        }
