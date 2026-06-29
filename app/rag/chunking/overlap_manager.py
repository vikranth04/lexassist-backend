from typing import List


class OverlapManager:
    """
    Manages configurable token overlaps between adjacent chunk blocks.
    """
    def __init__(self, overlap_tokens: int = 120):
        self.overlap_tokens = overlap_tokens

    def get_overlap_text(self, previous_sentences: List[str]) -> str:
        """Retrieves trailing sentence context to serve as the leading overlap of next chunk."""
        overlap_parts = []
        accumulated_tokens = 0

        # Traverse sentences backwards from end of current chunk
        for sentence in reversed(previous_sentences):
            # 1 token ~= 4 chars heuristic
            sentence_tokens = len(sentence) // 4
            if accumulated_tokens + sentence_tokens > self.overlap_tokens:
                break
            overlap_parts.insert(0, sentence)
            accumulated_tokens += sentence_tokens

        return " ".join(overlap_parts)
