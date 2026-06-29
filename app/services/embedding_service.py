from app.core.dependencies import get_gemini_service


class EmbeddingService:

    def __init__(self):
        self.gemini_service = get_gemini_service()

    def generate_embedding(self, text: str):
        return self.gemini_service.generate_embedding(text)