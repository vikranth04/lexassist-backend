from typing import List, Dict, Any
from app.core.exceptions import RankingException
from app.core.logger import logger


class SimilarityRanker:
    """
    Ranks retrieved chunks based on multiple relevance factors.

    Responsibilities:
    - Vector similarity score
    - Metadata relevance
    - Source quality
    - Document freshness (if available)
    - Section importance
    """

    def rank_results(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sorts the chunks list by a computed ranking score.
        """
        if not chunks:
            return []

        try:
            logger.info(f"Ranking {len(chunks)} results.")
            # Calculate a combined score for each chunk
            for chunk in chunks:
                chunk["ranking_score"] = self._calculate_score(chunk)

            # Sort by ranking_score descending
            return sorted(chunks, key=lambda ch: ch.get("ranking_score", 0.0), reverse=True)
        except Exception as e:
            logger.error(f"Ranking error: {str(e)}")
            raise RankingException(f"Similarity ranking sorting failed: {str(e)}")

    def _calculate_score(self, chunk: Dict[str, Any]) -> float:
        """
        Calculates a weighted score for a chunk.
        """
        similarity = chunk.get("similarity_score", 0.0)
        metadata = chunk.get("metadata", {})

        # 1. Base score is the similarity
        score = similarity

        # 2. Source quality boost (example)
        source_type = metadata.get("source_type")
        if source_type == "official_document":
            score += 0.05

        # 3. Document freshness boost (if date is present)
        # Simplified: just a placeholder for now
        if "date" in metadata:
            # logic to boost newer documents
            pass

        # 4. Section importance boost
        # e.g., chunks from 'Introduction' or 'Summary' might get a small boost
        heading = metadata.get("heading", "").lower()
        if any(h in heading for h in ["summary", "overview", "conclusion"]):
            score += 0.02

        return min(score, 1.0) # Cap at 1.0
