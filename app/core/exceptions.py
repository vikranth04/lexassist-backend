from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logger import logger


class AppBaseException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = 500, code: str = None):
        self.message = message
        self.status_code = status_code
        self.code = code or self.__class__.__name__
        super().__init__(message)


class EntityNotFoundException(AppBaseException):
    def __init__(self, message: str = "Entity not found"):
        super().__init__(message, status_code=404)


class ValidationException(AppBaseException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=400)


class SourceValidationException(AppBaseException):
    def __init__(self, message: str = "Source validation failed"):
        super().__init__(message, status_code=400)


class DuplicateSourceException(AppBaseException):
    def __init__(self, message: str = "Duplicate source detected"):
        super().__init__(message, status_code=409)


class InvalidSourceTypeException(AppBaseException):
    def __init__(self, message: str = "Invalid source type specified"):
        super().__init__(message, status_code=400)


class MetadataException(AppBaseException):
    def __init__(self, message: str = "Metadata generation failed"):
        super().__init__(message, status_code=500)


class RegistrationException(AppBaseException):
    def __init__(self, message: str = "Source registration failed"):
        super().__init__(message, status_code=500)


# Web Crawling & Scraping Exceptions
class WebsiteUnavailableException(AppBaseException):
    def __init__(self, message: str = "Website is unavailable"):
        super().__init__(message, status_code=503)


class CrawlException(AppBaseException):
    def __init__(self, message: str = "Crawling failed"):
        super().__init__(message, status_code=500)


class HTMLParsingException(AppBaseException):
    def __init__(self, message: str = "HTML parsing failed"):
        super().__init__(message, status_code=422)


class MetadataExtractionException(AppBaseException):
    def __init__(self, message: str = "Metadata extraction failed"):
        super().__init__(message, status_code=422)


class ContentExtractionException(AppBaseException):
    def __init__(self, message: str = "Content extraction failed"):
        super().__init__(message, status_code=422)


class URLValidationException(AppBaseException):
    def __init__(self, message: str = "URL validation failed"):
        super().__init__(message, status_code=400)


# PDF Processing Exceptions
class PDFValidationException(AppBaseException):
    def __init__(self, message: str = "PDF validation failed"):
        super().__init__(message, status_code=400)


class PDFParsingException(AppBaseException):
    def __init__(self, message: str = "PDF parsing failed"):
        super().__init__(message, status_code=422)


class PDFCorruptedException(AppBaseException):
    def __init__(self, message: str = "PDF file is corrupted"):
        super().__init__(message, status_code=400)


class PasswordProtectedPDFException(AppBaseException):
    def __init__(self, message: str = "PDF is password protected"):
        super().__init__(message, status_code=400)


class PageExtractionException(AppBaseException):
    def __init__(self, message: str = "PDF page extraction failed"):
        super().__init__(message, status_code=422)


class TextExtractionException(AppBaseException):
    def __init__(self, message: str = "PDF text extraction failed"):
        super().__init__(message, status_code=422)


# Text Normalization & Cleaning Exceptions
class TextNormalizationException(AppBaseException):
    def __init__(self, message: str = "Text normalization failed"):
        super().__init__(message, status_code=422)


class UnicodeNormalizationException(AppBaseException):
    def __init__(self, message: str = "Unicode normalization failed"):
        super().__init__(message, status_code=422)


class BoilerplateRemovalException(AppBaseException):
    def __init__(self, message: str = "Boilerplate removal failed"):
        super().__init__(message, status_code=422)


class DuplicateContentException(AppBaseException):
    def __init__(self, message: str = "Duplicate content detected"):
        super().__init__(message, status_code=409)


class ContentCleaningException(AppBaseException):
    def __init__(self, message: str = "Content cleaning failed"):
        super().__init__(message, status_code=422)


# Chunking Exceptions
class ChunkGenerationException(AppBaseException):
    def __init__(self, message: str = "Chunk generation failed"):
        super().__init__(message, status_code=500)


class ChunkValidationException(AppBaseException):
    def __init__(self, message: str = "Chunk validation failed"):
        super().__init__(message, status_code=400)


class SectionDetectionException(AppBaseException):
    def __init__(self, message: str = "Section detection failed"):
        super().__init__(message, status_code=422)


class SemanticSplitException(AppBaseException):
    def __init__(self, message: str = "Semantic splitting failed"):
        super().__init__(message, status_code=422)


class MetadataGenerationException(AppBaseException):
    def __init__(self, message: str = "Metadata builder step failed"):
        super().__init__(message, status_code=500)


# Embedding Pipeline Exceptions
class EmbeddingGenerationException(AppBaseException):
    def __init__(self, message: str = "Embedding vector generation failed"):
        super().__init__(message, status_code=500)


class EmbeddingProviderException(AppBaseException):
    def __init__(self, message: str = "Embedding API provider connection failed"):
        super().__init__(message, status_code=502)


class EmbeddingValidationException(AppBaseException):
    def __init__(self, message: str = "Embedding vector validation failed"):
        super().__init__(message, status_code=400)


class BatchProcessingException(AppBaseException):
    def __init__(self, message: str = "Batch vector processing failed"):
        super().__init__(message, status_code=500)


class EmbeddingCacheException(AppBaseException):
    def __init__(self, message: str = "Embedding cache check failed"):
        super().__init__(message, status_code=500)


# ChromaDB & Vector Store Exceptions
class VectorStoreException(AppBaseException):
    def __init__(self, message: str = "Vector database call failed"):
        super().__init__(message, status_code=500)


class CollectionException(AppBaseException):
    def __init__(self, message: str = "Collection management operation failed"):
        super().__init__(message, status_code=500)


class VectorValidationException(AppBaseException):
    def __init__(self, message: str = "Vector properties validation failed"):
        super().__init__(message, status_code=400)


class DuplicateVectorException(AppBaseException):
    def __init__(self, message: str = "Vector ID already exists inside database"):
        super().__init__(message, status_code=409)


class PersistenceException(AppBaseException):
    def __init__(self, message: str = "ChromaDB database serialization failed"):
        super().__init__(message, status_code=500)


class IndexingException(AppBaseException):
    def __init__(self, message: str = "Batch vector index operation failed"):
        super().__init__(message, status_code=500)


# RAG Retrieval Exceptions
class RetrievalException(AppBaseException):
    def __init__(self, message: str = "Vector search query retrieval failed"):
        super().__init__(message, status_code=500)


class SimilaritySearchException(AppBaseException):
    def __init__(self, message: str = "Similarity query search failed"):
        super().__init__(message, status_code=500)


class ContextBuilderException(AppBaseException):
    def __init__(self, message: str = "Context synthesis step failed"):
        super().__init__(message, status_code=500)


class MetadataFilterException(AppBaseException):
    def __init__(self, message: str = "Metadata filter validation failed"):
        super().__init__(message, status_code=400)


class CitationBuilderException(AppBaseException):
    def __init__(self, message: str = "Citation reference formatting failed"):
        super().__init__(message, status_code=500)


class RankingException(AppBaseException):
    def __init__(self, message: str = "Retrieval ranking sorting failed"):
        super().__init__(message, status_code=500)


# LLM & Groq Exceptions
class GroqConnectionException(AppBaseException):
    def __init__(self, message: str = "Groq API connection failed"):
        super().__init__(message, status_code=502)


class PromptValidationException(AppBaseException):
    def __init__(self, message: str = "Prompt validation failed"):
        super().__init__(message, status_code=400)


class ResponseValidationException(AppBaseException):
    def __init__(self, message: str = "LLM response validation failed"):
        super().__init__(message, status_code=500)


class TokenLimitException(AppBaseException):
    def __init__(self, message: str = "Token limit exceeded"):
        super().__init__(message, status_code=400)


class HallucinationException(AppBaseException):
    def __init__(self, message: str = "Potential hallucination detected"):
        super().__init__(message, status_code=500)


class CitationInjectionException(AppBaseException):
    def __init__(self, message: str = "Citation injection failed"):
        super().__init__(message, status_code=500)


async def app_exception_handler(request: Request, exc: AppBaseException):
    logger.error(f"App error: [{exc.code}] {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": None
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled system error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "InternalServerError",
                "message": "An unexpected error occurred.",
                "details": str(exc)
            }
        }
    )
