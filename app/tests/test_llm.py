import pytest
import time
from unittest.mock import MagicMock, patch, AsyncMock
from app.llm.prompt_builder import PromptBuilder
from app.llm.conversation_context import ConversationContext
from app.llm.gemini_service import GeminiService
from app.llm.response_validator import ResponseValidator
from app.llm.response_formatter import ResponseFormatter
from app.llm.citation_injector import CitationInjector
from app.llm.prompt_validator import PromptValidator

def test_prompt_builder():
    builder = PromptBuilder()
    prompt = builder.build_qa_prompt(
        question="What is law?",
        context="Law is a system of rules.",
        history="User: Hello\nAssistant: Hi",
        is_follow_up=True
    )
    assert "What is law?" in prompt["user_content"]
    assert "Law is a system of rules." in prompt["user_content"]
    assert "User: Hello" in prompt["user_content"]
    assert "You are LexAssist" in prompt["system_instruction"]

def test_conversation_context():
    ctx = ConversationContext()
    ctx.add_message("user", "Hello")
    ctx.add_message("assistant", "How can I help?")
    history_str = ctx.format_history()
    assert "User: Hello" in history_str
    assert "Assistant: How can I help?" in history_str

@pytest.mark.asyncio
@patch("google.genai.Client")
async def test_gemini_service(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_response = MagicMock()
    mock_response.text = "This is a test response."
    mock_client.models.generate_content.return_value = mock_response

    with patch("app.core.config.settings.GEMINI_API_KEY", "test-key"):
        service = GeminiService()
        response = await service.generate_response("test prompt")
        assert response == "This is a test response."

def test_response_validator():
    validator = ResponseValidator()
    # Should not raise
    validator.validate_response("Valid response text.")

    with pytest.raises(Exception):
        validator.validate_response("")

def test_response_formatter():
    formatter = ResponseFormatter()
    res = formatter.format_response(
        answer="Answer text",
        citations=[{"source": "test"}],
        conversation_id="123",
        start_time=time.time()
    )
    assert res["success"] is True
    assert res["answer"] == "Answer text"
    assert res["conversation_id"] == "123"
    assert "processing_time" in res

def test_citation_injector():
    injector = CitationInjector()
    citations = [{"source_id": "s1"}]
    injected = injector.inject_citations("According to Source 1...", citations)
    assert len(injected) == 1
    assert injected[0]["source_id"] == "s1"

def test_prompt_validator():
    validator = PromptValidator()
    # Should not raise
    validator.validate_prompt("System instruction", "User content")

    with pytest.raises(Exception):
        validator.validate_prompt("", "User content")
