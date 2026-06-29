from typing import Optional, Dict, Any
from app.rag.pipeline.pipeline_factory import PipelineFactory
from app.core.logger import logger

class ChatService:
    """
    High-level service for handling chat interactions.
    Now integrates with the Enterprise RAG Pipeline.
    """

    def __init__(self):
        # We instantiate the pipeline via factory
        self.rag_pipeline = PipelineFactory.create_rag_pipeline()

    async def chat(
        self,
        question: str,
        conversation_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Processes a user question through the enterprise RAG pipeline.
        """
        logger.info(f"Chat service processing question. Conversation ID: {conversation_id}")

        try:
            response = await self.rag_pipeline.chat(
                query=question,
                conversation_id=conversation_id,
                filters=filters
            )
            return response
        except Exception as e:
            logger.error(f"Chat service failure: {str(e)}")
            # Re-raise to be caught by API layer or exception handlers
            raise e
