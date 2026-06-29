import time
from typing import Dict, Any, List, Optional

class ResponseFormatter:
    """
    Standardizes the final API response format.
    """

    def format_response(
        self,
        answer: str,
        citations: List[Dict[str, Any]],
        conversation_id: str,
        start_time: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Constructs the final structured JSON response.
        """
        processing_time = time.time() - start_time

        return {
            "success": True,
            "answer": answer.strip(),
            "citations": citations,
            "conversation_id": conversation_id,
            "processing_time": f"{processing_time:.2f}s",
            "token_usage": {
                "total_tokens": 0, # To be filled if provider supports it
            },
            "metadata": metadata or {}
        }
