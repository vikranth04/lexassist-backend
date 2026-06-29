from typing import List, Dict, Any
from app.core.logger import logger

class SourceAttributor:
    """
    Transforms retrieved metadata into comprehensive source citations.

    Attributes:
    - URL/Title for Websites
    - Filename/Page/Heading for PDFs
    - Scores and IDs for traceability
    """

    def attribute_sources(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.info(f"Attributing {len(chunks)} sources.")

        attributions = []

        for chunk in chunks:
            metadata = chunk.get("metadata") or {}

            source_type = (
                metadata.get("source_type")
                or ("website" if metadata.get("source_information_original_filename_url") else "pdf")
            )

            source = {
                "source_type": source_type,
                "title": (
                    metadata.get("title")
                    or metadata.get("source_information_document_title")
                    or "Untitled Source"
                ),
                "website_url": (
                    metadata.get("website_url")
                    or metadata.get("source_information_original_filename_url")
                ),
                "pdf_filename": metadata.get("pdf_filename"),
            }

            location = {
                "page_number": (
                    metadata.get("page_number")
                    or metadata.get("location_page_number")
                ),
                "heading": (
                    metadata.get("heading")
                    or metadata.get("location_heading")
                ),
                "section": metadata.get("location_section_name"),
            }

            scores = {
                "similarity_score": round(chunk.get("similarity_score", 0), 4)
            }

            attributions.append({
                "source": source,
                "location": location,
                "scores": scores,
                "source_id": metadata.get("source_id"),
                "chunk_id": chunk.get("chunk_id"),
            })

        return attributions