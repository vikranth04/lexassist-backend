"""
RAG Retriever Module.
Responsible for querying the underlying vector stores or other indexing databases to extract
highly relevant text candidate chunks.
"""
from typing import List, Dict, Any, Optional
from app.rag.retrieval.retrieval_factory import RetrievalFactory


class RAGRetriever:
    """
    Retrieves candidate document/text chunks using the Enterprise Retrieval Pipeline.
    """
    def __init__(self, collection_name: Optional[str] = None):
        self.pipeline = RetrievalFactory.create_pipeline(collection_name=collection_name)

    async def retrieve(self, query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes the retrieval pipeline to return context and citations.
        """
        return await self.pipeline.run(query, filters=filters)
