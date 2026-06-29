from typing import Dict, Any


class DocumentAnalyzer:
    """
    Analyzes normalized documents and provides metadata-based chunking recommendations.
    """
    def analyze(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Runs page/character counts analysis and returns recommendations."""
        source_type = doc.get("source_type", "WEBSITE")
        clean_text = doc.get("clean_text") or ""
        char_count = len(clean_text)
        token_count = doc.get("estimated_token_count") or (char_count // 4)
        paragraph_count = doc.get("paragraph_count") or 0
        heading_count = doc.get("heading_count") or 0

        # Heuristic rules: select strategy depending on length bounds
        strategy = "semantic"
        if token_count > 8000:
            strategy = "section-aware-semantic"
        elif token_count < 1000:
            strategy = "paragraph-grouped"

        return {
            "source_type": source_type,
            "char_count": char_count,
            "token_count": token_count,
            "paragraph_count": paragraph_count,
            "heading_count": heading_count,
            "recommended_strategy": strategy
        }
