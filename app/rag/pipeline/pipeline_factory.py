from app.rag.pipeline.rag_pipeline import RAGPipeline
from app.rag.pipeline.conversation_manager import ConversationManager
from app.rag.pipeline.context_manager import ContextManager
from app.rag.pipeline.source_attributor import SourceAttributor
from app.rag.pipeline.response_manager import ResponseManager
from app.rag.retrieval.query_analyzer import QueryAnalyzer
from app.rag.retrieval.query_embedding import QueryEmbedding
from app.rag.retrieval.vector_search import VectorSearch
from app.rag.retrieval.metadata_filter import MetadataFilter
from app.rag.retrieval.similarity_ranker import SimilarityRanker
from app.rag.retrieval.deduplicator import Deduplicator
from app.rag.retrieval.retrieval_validator import RetrievalValidator
from app.llm.groq_service import GroqService
from app.llm.prompt_builder import PromptBuilder
from app.llm.response_validator import ResponseValidator
from app.llm.hallucination_guard import HallucinationGuard

class PipelineFactory:
    """
    Assembles the RAG pipeline with all required dependencies.
    """

    @staticmethod
    def create_rag_pipeline(collection_name: str = None) -> RAGPipeline:
        """
        Creates a production-ready RAGPipeline instance.
        """
        return RAGPipeline(
            conversation_manager=ConversationManager(),
            analyzer=QueryAnalyzer(),
            embedder=QueryEmbedding(),
            searcher=VectorSearch(collection_name=collection_name),
            filterer=MetadataFilter(),
            ranker=SimilarityRanker(),
            deduplicator=Deduplicator(),
            retrieval_validator=RetrievalValidator(),
            context_manager=ContextManager(),
            prompt_builder=PromptBuilder(),
            groq_service=GroqService(),
            response_validator=ResponseValidator(),
            hallucination_guard=HallucinationGuard(),
            source_attributor=SourceAttributor(),
            response_manager=ResponseManager()
        )
