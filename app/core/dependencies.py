from app.repositories.vector_repository import VectorRepository
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.file_repository import FileRepository
from app.repositories.source_repository import SourceRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.normalized_document_repository import NormalizedDocumentRepository
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.embedding_repository import EmbeddingRepository
from app.knowledge.source_registry import SourceRegistry
from app.knowledge.source_manager import SourceManager
from app.preprocessing.preprocessing_pipeline import PreprocessingPipeline
from app.rag.chunking.chunking_pipeline import ChunkingPipeline
from app.embeddings.embedding_pipeline import EmbeddingPipeline
from app.services.chat_service import ChatService
from app.services.website_service import WebsiteService
from app.services.conversation_service import ConversationService
from app.services.pdf_service import PDFService
from app.services.source_service import SourceService
from app.llm.groq_service import GroqService

# Lazy loaded singletons
_vector_repository = None
_conversation_repository = None
_file_repository = None
_source_repository = None
_document_repository = None
_normalized_document_repository = None
_chunk_repository = None
_embedding_repository = None
_source_registry = None
_source_manager = None
_preprocessing_pipeline = None
_chunking_pipeline = None
_embedding_pipeline = None
_groq_service = None
_chat_service = None
_website_service = None
_conversation_service = None
_pdf_service = None
_source_service = None


def get_vector_repository() -> VectorRepository:
    global _vector_repository
    if _vector_repository is None:
        _vector_repository = VectorRepository()
    return _vector_repository


def get_conversation_repository() -> ConversationRepository:
    global _conversation_repository
    if _conversation_repository is None:
        _conversation_repository = ConversationRepository()
    return _conversation_repository


def get_file_repository() -> FileRepository:
    global _file_repository
    if _file_repository is None:
        _file_repository = FileRepository()
    return _file_repository


def get_source_repository() -> SourceRepository:
    global _source_repository
    if _source_repository is None:
        _source_repository = SourceRepository()
    return _source_repository


def get_document_repository() -> DocumentRepository:
    global _document_repository
    if _document_repository is None:
        _document_repository = DocumentRepository()
    return _document_repository


def get_normalized_document_repository() -> NormalizedDocumentRepository:
    global _normalized_document_repository
    if _normalized_document_repository is None:
        _normalized_document_repository = NormalizedDocumentRepository()
    return _normalized_document_repository


def get_chunk_repository() -> ChunkRepository:
    global _chunk_repository
    if _chunk_repository is None:
        _chunk_repository = ChunkRepository()
    return _chunk_repository


def get_embedding_repository() -> EmbeddingRepository:
    global _embedding_repository
    if _embedding_repository is None:
        _embedding_repository = EmbeddingRepository()
    return _embedding_repository


def get_source_registry() -> SourceRegistry:
    global _source_registry
    if _source_registry is None:
        _source_registry = SourceRegistry()
    return _source_registry


def get_source_manager() -> SourceManager:
    global _source_manager
    if _source_manager is None:
        _source_manager = SourceManager(
            registry=get_source_registry(),
            repo=get_source_repository()
        )
    return _source_manager


def get_preprocessing_pipeline() -> PreprocessingPipeline:
    global _preprocessing_pipeline
    if _preprocessing_pipeline is None:
        _preprocessing_pipeline = PreprocessingPipeline()
    return _preprocessing_pipeline


def get_chunking_pipeline() -> ChunkingPipeline:
    global _chunking_pipeline
    if _chunking_pipeline is None:
        _chunking_pipeline = ChunkingPipeline()
    return _chunking_pipeline


def get_embedding_pipeline() -> EmbeddingPipeline:
    global _embedding_pipeline
    if _embedding_pipeline is None:
        _embedding_pipeline = EmbeddingPipeline()
    return _embedding_pipeline


def get_groq_service() -> GroqService:
    global _groq_service
    if _groq_service is None:
        _groq_service = GroqService()
    return _groq_service


def get_chat_service() -> ChatService:
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService()
    return _chat_service


def get_website_service() -> WebsiteService:
    global _website_service
    if _website_service is None:
        _website_service = WebsiteService(
            file_repo=get_file_repository(),
            doc_repo=get_document_repository(),
            preprocessing_pipeline=get_preprocessing_pipeline(),
            chunking_pipeline=get_chunking_pipeline(),
            embedding_pipeline=get_embedding_pipeline(),
            vector_repo=get_vector_repository()
        )
    return _website_service


def get_conversation_service() -> ConversationService:
    global _conversation_service
    if _conversation_service is None:
        _conversation_service = ConversationService(
            repo=get_conversation_repository()
        )
    return _conversation_service


def get_pdf_service() -> PDFService:
    global _pdf_service
    if _pdf_service is None:
        _pdf_service = PDFService(
            file_repo=get_file_repository(),
            doc_repo=get_document_repository(),
            preprocessing_pipeline=get_preprocessing_pipeline(),
            chunking_pipeline=get_chunking_pipeline(),
            embedding_pipeline=get_embedding_pipeline(),
            vector_repo=get_vector_repository()
        )
    return _pdf_service


def get_source_service() -> SourceService:
    global _source_service
    if _source_service is None:
        _source_service = SourceService(
            file_repo=get_file_repository(),
            vector_repo=get_vector_repository()
        )
    return _source_service
