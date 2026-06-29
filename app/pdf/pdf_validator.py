import os
from app.core.exceptions import PDFValidationException


class PDFValidator:
    """
    Validates PDF file attributes such as extension, presence, and sizes.
    """
    def validate(self, file_path: str, max_size_mb: int = 15) -> bool:
        """Validates PDF file details. Raises PDFValidationException on errors."""
        if not os.path.exists(file_path):
            raise PDFValidationException("Target PDF file does not exist on disk.")
        if not file_path.lower().endswith(".pdf"):
            raise PDFValidationException("Uploaded file does not have a PDF extension.")

        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb <= 0:
            raise PDFValidationException("PDF file size must be greater than zero.")
        if file_size_mb > max_size_mb:
            raise PDFValidationException(f"PDF file size exceeds the allowed threshold of {max_size_mb} MB.")
        return True
