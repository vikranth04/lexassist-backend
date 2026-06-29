import fitz
from typing import Dict, Any, List
from app.pdf.pdf_loader import PDFLoader
from app.pdf.pdf_validator import PDFValidator
from app.pdf.metadata_extractor import MetadataExtractor
from app.pdf.text_extractor import TextExtractor
from app.pdf.page_processor import PageProcessor
from app.pdf.structure_detector import StructureDetector
from app.pdf.text_cleaner import TextCleaner
from app.pdf.pdf_factory import PDFFactory
from app.core.exceptions import AppBaseException, PDFParsingException


class PDFParser:
    """
    Coordinates PDF validation, metadata discovery, page-level text parsing,
    cleaning, structural layout classification, and document standardization.
    """
    def __init__(self):
        self.loader = PDFLoader()
        self.validator = PDFValidator()
        self.metadata_extractor = MetadataExtractor()
        self.text_extractor = TextExtractor()
        self.page_processor = PageProcessor()
        self.structure_detector = StructureDetector()
        self.cleaner = TextCleaner()
        self.factory = PDFFactory()

    def parse(self, file_path: str, source_id: str) -> Dict[str, Any]:
        """Parses a local PDF file and returns a standardized document dictionary."""
        try:
            # Validate properties
            self.validator.validate(file_path)

            # Load document
            doc = self.loader.load(file_path)

            # Extract metadata
            metadata = self.metadata_extractor.extract(doc, file_path, source_id)

            pages_log = []
            for page_idx in range(len(doc)):
                page = doc.load_page(page_idx)
                raw_text = self.text_extractor.extract_text(page)

                # Format layout lines
                clean_text = self.cleaner.clean(raw_text)

                # Compute character counts and estimated tokens
                processed = self.page_processor.process_page(page_idx + 1, raw_text)

                # Detect layout groups (headings, lists)
                structure = self.structure_detector.detect_structure(clean_text)

                pages_log.append({
                    "page_number": page_idx + 1,
                    "clean_text": clean_text,
                    "character_count": processed["character_count"],
                    "estimated_token_count": processed["estimated_token_count"],
                    "structure": structure
                })

            # Package document representation
            document_package = self.factory.create_document(source_id, metadata, pages_log)

            doc.close()
            return document_package

        except AppBaseException as e:
            raise e
        except Exception as e:
            raise PDFParsingException(f"Failed to process and parse PDF contents: {str(e)}")
