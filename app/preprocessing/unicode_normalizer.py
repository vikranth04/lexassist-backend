import unicodedata
from app.core.exceptions import UnicodeNormalizationException


class UnicodeNormalizer:
    """
    Standardizes smart quotation marks, dash delimiters, and ensures clean UTF-8 NFKC characters.
    """
    def normalize(self, text: str) -> str:
        """Applies Unicode normalization rules to text. Raises UnicodeNormalizationException on error."""
        try:
            # Apply standard Compatibility Decomposition NFKC normalization
            normalized = unicodedata.normalize("NFKC", text)

            # Standardize typographic quotes and apostrophes
            normalized = normalized.replace("“", '"').replace("”", '"')
            normalized = normalized.replace("‘", "'").replace("’", "'")

            # Standardize dashes and hyphens
            normalized = normalized.replace("—", "-").replace("–", "-")

            return normalized
        except Exception as e:
            raise UnicodeNormalizationException(f"Unicode normalization failure: {str(e)}")
