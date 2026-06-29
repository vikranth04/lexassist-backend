import re


class TextCleaner:
    """
    Cleans PDF texts without degrading headings and listing structures.
    """
    def clean(self, text: str) -> str:
        """Strips control chars and extra horizontal spacing, keeping structure intact."""
        if not text:
            return ""
        # Remove non-printable control characters (excluding newlines/tabs)
        text = "".join(ch for ch in text if ch.isprintable() or ch in "\n\r\t")
        # Compress multiple spaces
        text = re.sub(r"[ \t]+", " ", text)
        # Compress blank lines to at most double newlines
        text = re.sub(r"\n\s*\n", "\n\n", text)
        return text.strip()
