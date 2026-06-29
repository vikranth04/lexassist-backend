import time
from typing import Dict, Any, Optional, List
from app.core.logger import logger
from app.core.exceptions import RetrievalException, GroqConnectionException
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
from app.llm.citation_injector import CitationInjector
from app.llm.hallucination_guard import HallucinationGuard
from app.rag.pipeline.conversation_manager import ConversationManager
from app.rag.pipeline.context_manager import ContextManager
from app.rag.pipeline.source_attributor import SourceAttributor
from app.rag.pipeline.response_manager import ResponseManager
from app.rag.pipeline.pipeline_orchestrator import PipelineOrchestrator
from app.rag.pipeline.performance_tracker import PerformanceTracker

class RAGPipeline:
    """
    The main enterprise orchestration layer for the RAG system.
    """

    def __init__(
        self,
        conversation_manager: ConversationManager,
        analyzer: QueryAnalyzer,
        embedder: QueryEmbedding,
        searcher: VectorSearch,
        filterer: MetadataFilter,
        ranker: SimilarityRanker,
        deduplicator: Deduplicator,
        retrieval_validator: RetrievalValidator,
        context_manager: ContextManager,
        prompt_builder: PromptBuilder,
        groq_service: GroqService,
        response_validator: ResponseValidator,
        hallucination_guard: HallucinationGuard,
        source_attributor: SourceAttributor,
        response_manager: ResponseManager
    ):
        self.conv_manager = conversation_manager
        self.analyzer = analyzer
        self.embedder = embedder
        self.searcher = searcher
        self.filterer = filterer
        self.ranker = ranker
        self.deduplicator = deduplicator
        self.retrieval_validator = retrieval_validator
        self.context_manager = context_manager
        self.prompt_builder = prompt_builder
        self.groq = groq_service
        self.response_validator = response_validator
        self.hallucination_guard = hallucination_guard
        self.source_attributor = source_attributor
        self.response_manager = response_manager

    async def chat(
        self,
        query: str,
        conversation_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes the full end-to-end RAG flow.
        """
        start_time = time.time()
        tracker = PerformanceTracker()
        orchestrator = PipelineOrchestrator(performance_tracker=tracker)

        logger.info(f"RAG Request received. Query: {query[:50]}...")

        # 1. Load Conversation
        conv_data = self.conv_manager.get_or_create_conversation(conversation_id)
        conv_id = conv_data["id"]
        memory = self.conv_manager.get_memory(conv_id)

        # 2. Analyze Query
        analysis = await orchestrator.execute_stage(
            "query_analysis", self.analyzer.analyze_query, query
        )

        # 3. Generate Embedding
        query_vector = await orchestrator.execute_stage(
            "query_embedding", self.embedder.embed_query, analysis["search_query"]
        )

        # 4. Retrieval & Processing
        chroma_filters = self.filterer.build_chroma_filter(filters)
        raw_chunks = await orchestrator.execute_stage(
            "vector_search", self.searcher.search_vectors, query_vector, filters=chroma_filters
        )

        ranked_chunks = self.ranker.rank_results(raw_chunks)
        unique_chunks = self.deduplicator.deduplicate(ranked_chunks)
        self.retrieval_validator.validate_results(unique_chunks)

        # 5. Build Context & Prompt
        context_str = self.context_manager.merge_and_format(unique_chunks)
        history_str = memory.format_history()

        prompt_package = self.prompt_builder.build_qa_prompt(
            question=query,
            context=context_str,
            history=history_str,
            is_follow_up=analysis.get("is_follow_up", False)
        )

        # 6. Groq Generation
        answer = await orchestrator.execute_stage(
            "groq_generation",
            self.groq.generate_response,
            prompt=prompt_package["user_content"],
            system_instruction=prompt_package["system_instruction"]
        )

        # 7. Response Validation & Guarding
        self.response_validator.validate_response(answer)
        self.hallucination_guard.check_response(answer, context_str)

        # 8. Source Attribution
        attributions = self.source_attributor.attribute_sources(unique_chunks)

        # 9. Update Conversation
        self.conv_manager.add_turn(conv_id, query, answer)

        # 10. Format Final Response
        retrieval_meta = {"chunk_count": len(unique_chunks)}
        final_response = self.response_manager.create_final_response(
            answer=answer,
            citations=attributions,
            conversation_id=conv_id,
            start_time=start_time,
            retrieval_meta=retrieval_meta
        )

        # Attach performance metrics to metadata
        final_response["metadata"]["performance"] = tracker.get_metrics()

        logger.info(f"RAG Request completed in {time.time() - start_time:.2f}s")
        import json

        logger.info("===== FINAL RESPONSE =====")
        logger.info(json.dumps(final_response, indent=2, default=str))
        return final_response
