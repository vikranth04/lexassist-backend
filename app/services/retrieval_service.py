from app.services.embedding_service import EmbeddingService
from app.core.dependencies import get_vector_repository


class RetrievalService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_repository = get_vector_repository()

    def retrieve(self, query: str, top_k: int = 5):
        """
        Retrieve the most relevant chunks for a user query.
        """

        # Generate embedding for the user's question
        query_embedding = self.embedding_service.generate_embedding(query)

        # Search repository
        results = self.vector_repository.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return results