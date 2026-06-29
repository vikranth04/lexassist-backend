"""
Legacy RAG Pipeline Module Bridge.
Points to the new Enterprise RAG Pipeline orchestration layer.
"""
from typing import Dict, Any, Optional
from app.rag.pipeline.pipeline_factory import PipelineFactory

class RAGPipeline:
    """
    Bridge class for the enterprise RAG pipeline.
    """
    def __init__(self, collection_name: Optional[str] = None):
        self.pipeline = PipelineFactory.create_rag_pipeline(collection_name=collection_name)

    async def run(
        self,
        query: str,
        conversation_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Runs the full end-to-end RAG flow.
        """
        return await self.pipeline.chat(query, conversation_id=conversation_id, filters=filters)
