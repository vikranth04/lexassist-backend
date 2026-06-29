import time
from typing import Dict, Any
from app.preprocessing.normalizer import Normalizer
from app.preprocessing.boilerplate_remover import BoilerplateRemover
from app.preprocessing.duplicate_detector import DuplicateDetector
from app.preprocessing.content_cleaner import ContentCleaner
from app.preprocessing.structure_preserver import StructurePreserver
from app.preprocessing.quality_validator import QualityValidator
from app.core.logger import logger


class PreprocessingPipeline:
    """
    Orchestrates the complete text preprocessing sequence.
    Output formats comply with the Standardized Output Model.
    """
    def __init__(self):
        self.normalizer = Normalizer()
        self.boilerplate_remover = BoilerplateRemover()
        self.duplicate_detector = DuplicateDetector()
        self.content_cleaner = ContentCleaner()
        self.structure_preserver = StructurePreserver()
        self.quality_validator = QualityValidator()

    def process(self, raw_document: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the raw document elements through normalization and returns the preprocessed package."""
        logger.info(f"Initiated preprocessing pipeline for doc: {raw_document.get('document_id')}")

        # Extract textual content from pages or main body
        raw_text = raw_document.get("clean_content") or ""
        if not raw_text and "pages" in raw_document:
            raw_text = "\n\n".join(page.get("clean_text", "") for page in raw_document["pages"])

        # 1. Normalize Unicode and whitespace
        normalized = self.normalizer.normalize(raw_text)

        # 2. Boilerplate removal
        no_boilerplate = self.boilerplate_remover.remove(normalized)

        # 3. Duplicate detection
        no_duplicates = self.duplicate_detector.remove_duplicates(no_boilerplate)

        # 4. Content cleaning
        clean_text = self.content_cleaner.clean(no_duplicates)

        # 5. Quality validation checks
        validation_report = self.quality_validator.validate(clean_text)

        # 6. Preserve heading/list hierarchies
        preserved_hierarchy = self.structure_preserver.preserve(raw_document.get("section_hierarchy") or [])

        # Standard metrics calculation
        paragraphs = [p for p in clean_text.split("\n\n") if p.strip()]

        normalized_document = {
            "source_id": raw_document.get("source_id"),
            "document_id": raw_document.get("document_id"),
            "source_type": raw_document.get("metadata", {}).get("source_type", "WEBSITE"),
            "original_filename_url": raw_document.get("url") or raw_document.get("metadata", {}).get("filename"),
            "clean_text": clean_text,
            "section_hierarchy": preserved_hierarchy,
            "paragraph_count": len(paragraphs),
            "heading_count": len(preserved_hierarchy),
            "character_count": validation_report["character_count"],
            "estimated_token_count": validation_report["estimated_token_count"],
            "processing_timestamp": float(time.time()),
            "cleaning_version": "1.0.0",
            "validation_result": validation_report
        }

        logger.info(f"Preprocessing pipeline completed successfully for doc: {raw_document.get('document_id')}")
        return normalized_document
