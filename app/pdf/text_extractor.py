import fitz


class TextExtractor:
    """
    Handles plain layout text extraction from fitz Page blocks.
    """
    def extract_text(self, page: fitz.Page) -> str:
        """Extracts raw text content from the specified page object."""
        # Retrieve text block layout formatting
        text = page.get_text("text")
        return text if text else ""
