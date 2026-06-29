from typing import Dict, Any


class PageProcessor:
    """
    Computes page-specific metrics such as character count and estimated tokens.
    """
    def process_page(self, page_num: int, raw_text: str) -> Dict[str, Any]:
        """Calculates page metrics and constructs structured metadata."""
        char_count = len(raw_text)
        # Token estimation: standard heuristic of ~4 characters per token
        estimated_tokens = char_count // 4

        return {
            "page_number": page_num,
            "raw_text": raw_text,
            "character_count": char_count,
            "estimated_token_count": estimated_tokens
        }
