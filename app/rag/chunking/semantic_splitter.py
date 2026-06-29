import re
from typing import List
from app.core.exceptions import SemanticSplitException


class SemanticSplitter:
    """
    Groups clean text blocks into logical sentences without breaking lists or abbreviations.
    """
    def split_sentences(self, text: str) -> List[str]:
        """Splits text by sentence punctuation. Raises SemanticSplitException on error."""
        try:
            if not text:
                return []
            # Split sentence markers, avoiding initials and decimal numbers
            sentence_ends = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
            sentences = [s.strip() for s in sentence_ends.split(text) if s.strip()]
            return sentences
        except Exception as e:
            raise SemanticSplitException(f"Semantic sentence segmentation failed: {str(e)}")
