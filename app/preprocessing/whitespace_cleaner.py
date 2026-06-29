import re
from app.core.exceptions import TextNormalizationException


class WhitespaceCleaner:
    """
    Cleans consecutive space markers, tabs, and preserves single blank paragraph lines.
    """
    def clean(self, text: str) -> str:
        """Compresses whitespace inside the text content. Raises TextNormalizationException on error."""
        try:
            lines = [line.strip() for line in text.split("\n")]
            cleaned_lines = []
            consecutive_empty = 0

            for line in lines:
                if not line:
                    consecutive_empty += 1
                    # Allow at most one blank line between paragraphs
                    if consecutive_empty <= 1:
                        cleaned_lines.append("")
                else:
                    consecutive_empty = 0
                    # Compress duplicate horizontal spacing
                    compressed = re.sub(r"[ \t]+", " ", line)
                    cleaned_lines.append(compressed)

            return "\n".join(cleaned_lines).strip()
        except Exception as e:
            raise TextNormalizationException(f"Whitespace cleaning error: {str(e)}")
