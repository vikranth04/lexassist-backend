from app.preprocessing.unicode_normalizer import UnicodeNormalizer
from app.preprocessing.whitespace_cleaner import WhitespaceCleaner


class Normalizer:
    """
    Consolidates Unicode and Whitespace cleaning steps into a single normalization step.
    """
    def __init__(self):
        self.unicode_normalizer = UnicodeNormalizer()
        self.whitespace_cleaner = WhitespaceCleaner()

    def normalize(self, text: str) -> str:
        """Runs Unicode followed by Whitespace normalization."""
        text = self.unicode_normalizer.normalize(text)
        text = self.whitespace_cleaner.clean(text)
        return text
