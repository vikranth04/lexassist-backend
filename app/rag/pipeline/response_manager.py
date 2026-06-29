import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.core.logger import logger

class ResponseManager:
    """
    Standardizes the RAG pipeline output for the frontend.
    """

    def create_final_response(
        self,
        answer: str,
        citations: List[Dict[str, Any]],
        conversation_id: str,
        start_time: float,
        retrieval_meta: Dict[str, Any],
        model: str = "gemini-2.5-flash"
    ) -> Dict[str, Any]:
        """
        Builds the unified response structure.
        """
        processing_time_ms = int((time.time() - start_time) * 1000)

        return {
            "success": True,
            "conversation_id": conversation_id,
            "answer": answer.strip(),
            "citations": citations,
            "processing_time_ms": processing_time_ms,
            "token_usage": {
                "prompt_tokens": 0,    # Placeholder
                "completion_tokens": 0, # Placeholder
                "total_tokens": 0
            },
            "retrieval": {
                "chunks_found": retrieval_meta.get("chunk_count", 0),
                "sources_used": len(set(c.get("source_id") for c in citations if c.get("source_id")))
            },
            "metadata": {
                "model": model,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
