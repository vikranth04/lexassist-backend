import fitz  # PyMuPDF
from app.core.exceptions import PDFCorruptedException, PasswordProtectedPDFException


class PDFLoader:
    """
    Safely loads a PDF document and checks for encryption and corruption.
    """
    def load(self, file_path: str) -> fitz.Document:
        """Loads and returns a fitz.Document. Raises PDFCorruptedException or PasswordProtectedPDFException."""
        try:
            doc = fitz.open(file_path)
            if doc.is_encrypted:
                raise PasswordProtectedPDFException("PDF document is password protected.")
            return doc
        except PasswordProtectedPDFException as e:
            raise e
        except Exception as e:
            raise PDFCorruptedException(f"PDF loading failed: file might be corrupted. {str(e)}")
