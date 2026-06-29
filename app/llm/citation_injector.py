from typing import List, Dict, Any
from app.core.exceptions import CitationInjectionException
from app.core.logger import logger

class CitationInjector:
    """
    Ensures citations from retrieval results are preserved and properly formatted in the response.
    """

    def inject_citations(self, response_text: str, retrieval_citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Maps citations used in the response text back to full citation metadata.
        """
        try:
            logger.info("Injecting full citation metadata into response.")
            used_citations = []

            # Simple heuristic: find [Source X] in text and include corresponding metadata
            for i, citation in enumerate(retrieval_citations):
                source_label = f"Source {i+1}"
                if source_label in response_text:
                    used_citations.append(citation)

            # If no explicit Source labels found, but citations exist, maybe include all as "referenced"
            if not used_citations and retrieval_citations:
                logger.info("No explicit source labels found in text, including all retrieved citations as references.")
                used_citations = retrieval_citations

            return used_citations
        except Exception as e:
            logger.error(f"Citation injection error: {str(e)}")
            raise CitationInjectionException(f"Failed to map citations: {str(e)}")
