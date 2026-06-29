from typing import Dict, List, Optional


class EmbeddingCache:
    """
    In-memory cache for vector representations to avoid redundant API request calls.
    """
    def __init__(self):
        self._cache: Dict[str, List[float]] = {}

    def get(self, text: str) -> Optional[List[float]]:
        """Checks if vector exists in cache."""
        return self._cache.get(text)

    def set(self, text: str, vector: List[float]):
        """Caches text-vector pair."""
        self._cache[text] = vector

    def invalidate(self):
        """Clears cache."""
        self._cache.clear()
