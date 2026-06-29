from typing import List, Dict, Any
from app.core.exceptions import CitationBuilderException
from app.core.logger import logger


class CitationBuilder:
    """
    Prepares structured citation information for retrieved chunks.

    Responsibilities:
    - Format document, source, and location information
    - Include relevance scores
    """

    def build_citations(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Creates a list of structured citation objects.
        """
        try:
            logger.info(f"Building citations for {len(chunks)} chunks.")
            citations = []

            for chunk in chunks:
                metadata = chunk.get("metadata", {})

                citation = {
                    "document": {
                        "source_id": metadata.get("source_id"),
                        "document_id": metadata.get("document_id"),
                        "chunk_id": chunk.get("chunk_id")
                    },
                    "source": {
                        "source_type": metadata.get("source_type"),
                        "website_url": metadata.get("website_url"),
                        "pdf_filename": metadata.get("pdf_filename")
                    },
                    "location": {
                        "page_number": metadata.get("page_number"),
                        "heading": metadata.get("heading"),
                        "section": metadata.get("section")
                    },
                    "scores": {
                        "similarity_score": chunk.get("similarity_score"),
                        "ranking_score": chunk.get("ranking_score")
                    }
                }
                citations.append(citation)

            return citations
        except Exception as e:
            logger.error(f"Citation building failure: {str(e)}")
            raise CitationBuilderException(f"Citation reference formatting failed: {str(e)}")
