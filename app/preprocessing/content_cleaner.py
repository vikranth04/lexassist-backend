from app.core.exceptions import ContentCleaningException


class ContentCleaner:
    """
    Strips raw code remnants and non-printable text fragments.
    """
    def clean(self, text: str) -> str:
        """Runs content structural cleanup rules. Raises ContentCleaningException on error."""
        try:
            # Strip non-printable ascii details
            text = "".join(c for c in text if c.isprintable() or c in "\n\r\t")
            return text.strip()
        except Exception as e:
            raise ContentCleaningException(f"Content cleaning failure: {str(e)}")
