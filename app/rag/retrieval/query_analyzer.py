import re
from typing import Dict, Any, List


class QueryAnalyzer:
    """
    Analyzes user queries to improve retrieval quality.

    Responsibilities:
    - Normalize user questions
    - Detect question intent
    - Extract important keywords
    - Identify legal entities
    - Estimate query complexity
    - Detect follow-up questions
    - Prepare search query
    """

    LEGAL_KEYWORDS = [
        "section", "article", "clause", "law", "statute", "court", "contract",
        "agreement", "provision", "regulation", "legal", "liability", "compliance"
    ]

    ENTITY_PATTERNS = [
        r"Section\s+\d+",
        r"Article\s+\d+",
        r"Chapter\s+\d+",
        r"Act\s+of\s+\d{4}",
        r"[A-Z][a-z]+\s+v\.\s+[A-Z][a-z]+"  # Case name like Smith v. Jones
    ]

    FOLLOW_UP_INDICATORS = [
        "it", "they", "that", "this", "he", "she", "more", "tell me more", "explain further"
    ]

    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyzes a query string and returns a structured analysis result.
        """
        normalized = self._normalize(query)
        intent = self._detect_intent(normalized)
        keywords = self._extract_keywords(normalized)
        entities = self._identify_entities(query)
        complexity = self._estimate_complexity(normalized)
        is_follow_up = self._detect_follow_up(normalized)
        search_query = self._prepare_search_query(normalized, keywords, entities)

        return {
            "original_query": query,
            "normalized_query": normalized,
            "search_query": search_query,
            "intent": intent,
            "keywords": keywords,
            "entities": entities,
            "complexity": complexity,
            "is_follow_up": is_follow_up
        }

    def _normalize(self, query: str) -> str:
        """Lowercases and strips the query."""
        return query.strip().lower()

    def _detect_intent(self, normalized: str) -> str:
        """Detects the intent of the query."""
        if any(term in normalized for term in self.LEGAL_KEYWORDS):
            return "legal_reference_query"

        if normalized.startswith(("how", "what", "why", "when", "where", "who")):
            return "informational_query"

        return "general_query"

    def _extract_keywords(self, normalized: str) -> List[str]:
        """Extracts keywords from the query."""
        # Simple stopword-like filtering (removes very short words)
        tokens = re.findall(r'\b\w{4,}\b', normalized)
        return list(set(tokens))

    def _identify_entities(self, query: str) -> List[str]:
        """Identifies potential legal entities using regex."""
        entities = []
        for pattern in self.ENTITY_PATTERNS:
            matches = re.findall(pattern, query, re.IGNORECASE)
            entities.extend(matches)
        return list(set(entities))

    def _estimate_complexity(self, normalized: str) -> str:
        """Estimates query complexity based on length and keywords."""
        token_count = len(normalized.split())
        if token_count > 15:
            return "high"
        elif token_count > 7:
            return "medium"
        return "low"

    def _detect_follow_up(self, normalized: str) -> bool:
        """Detects if the query is likely a follow-up."""
        # This is a very basic implementation.
        # Future expansion should use conversation history.
        return normalized.lower() in self.FOLLOW_UP_INDICATORS or normalized.startswith(("also", "and", "but"))

    def _prepare_search_query(self, normalized: str, keywords: List[str], entities: List[str]) -> str:
        """Prepares the actual query string for vector search."""
        # Combine entities and keywords for a more focused search
        return " ".join(entities + keywords) if entities or keywords else normalized
