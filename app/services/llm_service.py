from app.core.dependencies import get_gemini_service
from app.llm.prompt_builder import PromptBuilder
from app.llm.response_formatter import ResponseFormatter


class LLMService:

    def __init__(self):
        self.gemini_service = get_gemini_service()
        self.prompt_builder = PromptBuilder()
        self.response_formatter = ResponseFormatter()

    def generate_answer(self, question: str, context: str) -> str:
        prompt = self.prompt_builder.build_chat_prompt(question, context)
        answer = self.gemini_service.generate(prompt)
        return answer