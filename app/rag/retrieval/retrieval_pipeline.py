from typing import Dict, Any, Optional, List
from app.rag.retrieval.query_analyzer import QueryAnalyzer
from app.rag.retrieval.query_embedding import QueryEmbedding
from app.rag.retrieval.vector_search import VectorSearch
from app.rag.retrieval.metadata_filter import MetadataFilter
from app.rag.retrieval.similarity_ranker import SimilarityRanker
from app.rag.retrieval.deduplicator import Deduplicator
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.citation_builder import CitationBuilder
from app.rag.retrieval.retrieval_validator import RetrievalValidator
from app.core.logger import logger


class RetrievalPipeline:
    """
    Orchestrates the enterprise retrieval & context building process.

    Follows the flow:
    Analyze -> Embed -> Search -> Filter -> Rank -> Deduplicate -> Build Context -> Build Citations
    """

    def __init__(
        self,
        analyzer: QueryAnalyzer,
        embedder: QueryEmbedding,
        searcher: VectorSearch,
        filterer: MetadataFilter,
        ranker: SimilarityRanker,
        deduplicator: Deduplicator,
        context_builder: ContextBuilder,
        citation_builder: CitationBuilder,
        validator: RetrievalValidator
    ):
        self.analyzer = analyzer
        self.embedder = embedder
        self.searcher = searcher
        self.filterer = filterer
        self.ranker = ranker
        self.deduplicator = deduplicator
        self.context_builder = context_builder
        self.citation_builder = citation_builder
        self.validator = validator

    async def run(self, user_query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes the full retrieval pipeline.
        """
        logger.info(f"Starting retrieval pipeline for query: '{user_query}'")

        # 1. Query Analysis
        analysis = self.analyzer.analyze_query(user_query)
        logger.info(f"Query analyzed. Intent: {analysis['intent']}")

        # 2. Query Embedding
        query_vector = self.embedder.embed_query(analysis["search_query"])
        logger.info("Query embedding generated.")

        # 3. Vector Search & Metadata Filtering
        # (Filtering is partially integrated in searcher via ChromaDB 'where' clause)
        chroma_filters = self.filterer.build_chroma_filter(filters)
        raw_chunks = self.searcher.search_vectors(query_vector, filters=chroma_filters)
        logger.info(f"Retrieved {len(raw_chunks)} raw chunks.")

        # 4. Post-retrieval Filtering (if any additional logic needed)
        filtered_chunks = self.filterer.filter_results(raw_chunks, filters)

        # 5. Similarity Ranking
        ranked_chunks = self.ranker.rank_results(filtered_chunks)

        # 6. Duplicate Removal
        unique_chunks = self.deduplicator.deduplicate(ranked_chunks)

        # 7. Retrieval Validation
        self.validator.validate_results(unique_chunks)

        # 8. Context Building
        final_context = self.context_builder.build_context(unique_chunks)

        # 9. Citation Preparation
        citations = self.citation_builder.build_citations(unique_chunks)

        logger.info("Retrieval pipeline completed successfully.")

        return {
            "query_analysis": analysis,
            "context": final_context,
            "citations": citations,
            "metadata": {
                "chunk_count": len(unique_chunks),
                "total_raw_retrieved": len(raw_chunks)
            }
        }
