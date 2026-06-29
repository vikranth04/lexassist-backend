import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.rag.pipeline.pipeline_factory import PipelineFactory
from app.core.exceptions import RetrievalException

@pytest.mark.asyncio
@patch("app.rag.retrieval.query_embedding.QueryEmbedding.embed_query")
@patch("app.rag.retrieval.vector_search.VectorSearch.search_vectors")
@patch("app.llm.gemini_service.GeminiService.generate_response")
async def test_full_rag_pipeline_success(mock_gemini, mock_search, mock_embed):
    # Setup mocks
    mock_embed.return_value = [0.1] * 768
    mock_search.return_value = [
        {
            "chunk_id": "c1",
            "content": "The legal age is 18.",
            "metadata": {"source_id": "s1", "source_type": "pdf", "pdf_filename": "law.pdf", "page_number": 5},
            "similarity_score": 0.95
        }
    ]
    mock_gemini.return_value = "According to the document, the legal age is 18 [Source 1]."

    # Create pipeline
    pipeline = PipelineFactory.create_rag_pipeline()

    # Execute chat
    response = await pipeline.chat("What is the legal age?")

    # Assertions
    assert response["success"] is True
    assert "legal age is 18" in response["answer"]
    assert len(response["citations"]) == 1
    assert response["citations"][0]["pdf"]["filename"] == "law.pdf"
    assert "performance" in response["metadata"]
    assert response["retrieval"]["chunks_found"] == 1

@pytest.mark.asyncio
@patch("app.rag.retrieval.vector_search.VectorSearch.search_vectors")
async def test_rag_pipeline_no_results(mock_search):
    mock_search.return_value = []

    pipeline = PipelineFactory.create_rag_pipeline()

    # Should not crash, but return a "no info" type answer (handled by prompt templates)
    # Actually, RetrievalValidator might raise exception if configured to reject empty.
    # In Phase 9.8 implementation, I made it log a warning but not raise.

    with patch("app.llm.gemini_service.GeminiService.generate_response", new_callable=AsyncMock) as mock_gemini:
        mock_gemini.return_value = "I couldn't find information about that."
        response = await pipeline.chat("Unknown topic")

    assert response["success"] is True
    assert response["retrieval"]["chunks_found"] == 0

@pytest.mark.asyncio
@patch("app.llm.gemini_service.GeminiService.generate_response")
async def test_rag_pipeline_gemini_failure(mock_gemini):
    mock_gemini.side_effect = Exception("API connection failed")

    # Mock retrieval to avoid actual DB call
    with patch("app.rag.retrieval.query_embedding.QueryEmbedding.embed_query", return_value=[0.1]*768):
        with patch("app.rag.retrieval.vector_search.VectorSearch.search_vectors", return_value=[]):
            pipeline = PipelineFactory.create_rag_pipeline()

            with pytest.raises(Exception) as exc:
                await pipeline.chat("Hello")

            assert "API connection failed" in str(exc.value)
