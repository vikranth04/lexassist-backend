import re
from typing import List, Dict, Any


class StructureDetector:
    """
    Detects basic document structural types (headings, numbered lists, paragraph blocks)
    using text pattern heuristics.
    """
    def detect_structure(self, text: str) -> List[Dict[str, Any]]:
        """Scans page text lines and labels structural types."""
        elements = []
        lines = text.split("\n")

        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue

            # Heuristics: uppercase lines as headings
            if trimmed.isupper() and len(trimmed) < 70:
                elements.append({"type": "heading", "text": trimmed})
            # Numbered lists matching "1. ", "2) "
            elif re.match(r"^\d+[\.\)]\s+", trimmed):
                elements.append({"type": "numbered_list_item", "text": trimmed})
            # Bullet items
            elif trimmed.startswith("- ") or trimmed.startswith("* ") or trimmed.startswith("• "):
                elements.append({"type": "bullet_list_item", "text": trimmed})
            else:
                elements.append({"type": "paragraph", "text": trimmed})

        return elements
