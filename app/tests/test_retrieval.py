import pytest
from unittest.mock import MagicMock, patch
from app.rag.retrieval.query_analyzer import QueryAnalyzer
from app.rag.retrieval.query_embedding import QueryEmbedding
from app.rag.retrieval.vector_search import VectorSearch
from app.rag.retrieval.metadata_filter import MetadataFilter
from app.rag.retrieval.similarity_ranker import SimilarityRanker
from app.rag.retrieval.deduplicator import Deduplicator
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.citation_builder import CitationBuilder
from app.rag.retrieval.retrieval_pipeline import RetrievalPipeline
from app.rag.retrieval.retrieval_factory import RetrievalFactory

def test_query_analyzer():
    analyzer = QueryAnalyzer()
    result = analyzer.analyze_query("What are the legal requirements for a contract in Section 5?")
    assert result["intent"] == "legal_reference_query"
    assert "Section 5" in result["entities"]
    assert "contract" in result["keywords"]
    assert result["complexity"] == "medium"

@patch("app.embeddings.embedding_factory.EmbeddingFactory.get_provider")
def test_query_embedding(mock_get_provider):
    mock_provider = MagicMock()
    mock_provider.generate_embeddings.return_value = [[0.1] * 768]
    mock_get_provider.return_value = mock_provider

    embedder = QueryEmbedding()
    vector = embedder.embed_query("test query")
    assert len(vector) == 768
    assert vector[0] == 0.1

def test_metadata_filter():
    filterer = MetadataFilter()
    chunks = [
        {"metadata": {"source_type": "pdf", "page_number": 1}},
        {"metadata": {"source_type": "website", "url": "http://test.com"}}
    ]
    filters = {"source_type": "pdf"}
    filtered = filterer.filter_results(chunks, filters)
    assert len(filtered) == 1
    assert filtered[0]["metadata"]["source_type"] == "pdf"

def test_similarity_ranker():
    ranker = SimilarityRanker()
    chunks = [
        {"similarity_score": 0.5, "metadata": {}},
        {"similarity_score": 0.8, "metadata": {}},
        {"similarity_score": 0.6, "metadata": {"heading": "Summary"}}
    ]
    ranked = ranker.rank_results(chunks)
    assert ranked[0]["similarity_score"] == 0.8
    # 0.6 + 0.02 boost for Summary = 0.62, which is > 0.5
    assert ranked[1]["similarity_score"] == 0.6

def test_deduplicator():
    deduplicator = Deduplicator()
    chunks = [
        {"chunk_id": "1", "content": "same content"},
        {"chunk_id": "2", "content": "same content"},
        {"chunk_id": "3", "content": "different content"}
    ]
    unique = deduplicator.deduplicate(chunks)
    assert len(unique) == 2

def test_context_builder():
    builder = ContextBuilder()
    chunks = [
        {"content": "Chunk 1", "metadata": {"source_id": "s1", "page_number": 1}},
        {"content": "Chunk 2", "metadata": {"source_id": "s1", "page_number": 2}}
    ]
    context = builder.build_context(chunks)
    assert "Chunk 1" in context
    assert "Chunk 2" in context
    assert "Source 1" in context

def test_citation_builder():
    builder = CitationBuilder()
    chunks = [
        {
            "chunk_id": "c1",
            "similarity_score": 0.9,
            "ranking_score": 0.95,
            "metadata": {"source_id": "s1", "source_type": "pdf", "pdf_filename": "test.pdf"}
        }
    ]
    citations = builder.build_citations(chunks)
    assert len(citations) == 1
    assert citations[0]["document"]["chunk_id"] == "c1"
    assert citations[0]["source"]["pdf_filename"] == "test.pdf"

@pytest.mark.asyncio
@patch("app.rag.retrieval.query_embedding.QueryEmbedding.embed_query")
@patch("app.rag.retrieval.vector_search.VectorSearch.search_vectors")
async def test_retrieval_pipeline(mock_search, mock_embed):
    mock_embed.return_value = [0.1] * 768
    mock_search.return_value = [
        {
            "chunk_id": "c1",
            "content": "Relevant legal text",
            "metadata": {"source_id": "s1", "source_type": "legal"},
            "similarity_score": 0.9
        }
    ]

    pipeline = RetrievalFactory.create_pipeline()
    result = await pipeline.run("What is the law?")

    assert "context" in result
    assert "citations" in result
    assert result["metadata"]["chunk_count"] == 1
    assert "Relevant legal text" in result["context"]
