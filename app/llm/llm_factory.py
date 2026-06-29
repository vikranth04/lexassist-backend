from app.llm.groq_service import GroqService
from app.llm.prompt_builder import PromptBuilder
from app.llm.prompt_validator import PromptValidator
from app.llm.response_validator import ResponseValidator
from app.llm.response_formatter import ResponseFormatter
from app.llm.citation_injector import CitationInjector
from app.llm.hallucination_guard import HallucinationGuard

class LLMFactory:
    """
    Factory for creating LLM-related services.
    """

    @staticmethod
    def create_groq_service() -> GroqService:
        return GroqService()

    @staticmethod
    def create_prompt_builder() -> PromptBuilder:
        return PromptBuilder()

    @staticmethod
    def create_prompt_validator() -> PromptValidator:
        return PromptValidator()

    @staticmethod
    def create_response_validator() -> ResponseValidator:
        return ResponseValidator()

    @staticmethod
    def create_response_formatter() -> ResponseFormatter:
        return ResponseFormatter()

    @staticmethod
    def create_citation_injector() -> CitationInjector:
        return CitationInjector()

    @staticmethod
    def create_hallucination_guard() -> HallucinationGuard:
        return HallucinationGuard()
