from typing import Dict, Any, List
from app.core.exceptions import SectionDetectionException


class SectionDetector:
    """
    Extracts heading layout hierarchies to locate physical section transition points.
    """
    def detect_sections(self, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extracts and formats section nodes list. Raises SectionDetectionException on error."""
        try:
            # Returns the hierarchy extracted in Phase 9.4 Preprocessing
            return doc.get("section_hierarchy") or []
        except Exception as e:
            raise SectionDetectionException(f"Failed detecting sections layout: {str(e)}")
