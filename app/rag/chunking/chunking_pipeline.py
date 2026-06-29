from typing import Dict, Any, List
from app.rag.chunking.document_analyzer import DocumentAnalyzer
from app.rag.chunking.section_detector import SectionDetector
from app.rag.chunking.chunk_generator import ChunkGenerator
from app.core.logger import logger


class ChunkingPipeline:
    """
    Orchestrates the workflow: Document Analysis -> Section Boundaries -> Chunk Splitting -> Validator verification.
    """
    def __init__(self):
        self.analyzer = DocumentAnalyzer()
        self.section_detector = SectionDetector()
        self.generator = ChunkGenerator()

    def process(self, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Processes normalized document and returns segmented chunks list."""
        doc_id = doc.get("document_id", "unknown")
        logger.info(f"Initiated chunking pipeline for doc: {doc_id}")

        # Step 1: Run document structural properties analysis
        analysis = self.analyzer.analyze(doc)
        logger.info(f"Doc Analysis recommendations: {analysis.get('recommended_strategy')}")

        # Step 2: Detect section heading markers
        sections = self.section_detector.detect_sections(doc)
        logger.info(f"Located section headers count: {len(sections)}")

        # Step 3: Segment text lines
        chunks = self.generator.generate_chunks(doc)
        logger.info(f"Chunking pipeline completed. Total chunk files built: {len(chunks)}")

        return chunks
