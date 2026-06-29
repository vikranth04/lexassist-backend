from app.rag.retrieval.query_analyzer import QueryAnalyzer
from app.rag.retrieval.query_embedding import QueryEmbedding
from app.rag.retrieval.vector_search import VectorSearch
from app.rag.retrieval.metadata_filter import MetadataFilter
from app.rag.retrieval.similarity_ranker import SimilarityRanker
from app.rag.retrieval.deduplicator import Deduplicator
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.citation_builder import CitationBuilder
from app.rag.retrieval.retrieval_validator import RetrievalValidator
from app.rag.retrieval.retrieval_pipeline import RetrievalPipeline


class RetrievalFactory:
    """
    Factory for creating the RetrievalPipeline with all its dependencies.
    """

    @staticmethod
    def create_pipeline(collection_name: str = None) -> RetrievalPipeline:
        """
        Instantiates and returns a RetrievalPipeline.
        """
        return RetrievalPipeline(
            analyzer=QueryAnalyzer(),
            embedder=QueryEmbedding(),
            searcher=VectorSearch(collection_name=collection_name),
            filterer=MetadataFilter(),
            ranker=SimilarityRanker(),
            deduplicator=Deduplicator(),
            context_builder=ContextBuilder(),
            citation_builder=CitationBuilder(),
            validator=RetrievalValidator()
        )
