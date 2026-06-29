from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Optional


class Settings(BaseSettings):
    # Google Gemini (Used for Embeddings)
    GEMINI_API_KEY: str
    EMBEDDING_MODEL: str = "text-embedding-004"

    # Groq (Used for Chat Generation)
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # ChromaDB
    CHROMA_DB_PATH: str = "./chroma_db"

    # Text Chunking
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Production limits & settings
    MAX_UPLOAD_SIZE_MB: int = 15
    ALLOWED_EXTENSIONS: list[str] = [".pdf"]
    CORS_ORIGINS: list[str] = ["*"]

    # Embedding configurations
    EMBEDDING_PROVIDER: str = "gemini"
    EMBEDDING_BATCH_SIZE: int = 16
    EMBEDDING_RETRY_COUNT: int = 3
    EMBEDDING_TIMEOUT: int = 30

    # ChromaDB Vector Store configurations
    VECTOR_COLLECTION_NAME: str = "legal_documents"
    VECTOR_BATCH_SIZE: int = 64
    VECTOR_RETRY_COUNT: int = 3
    VECTOR_TIMEOUT: int = 30

    # RAG Retrieval configurations
    RAG_TOP_K: int = 5
    RAG_SIMILARITY_THRESHOLD: float = 0.4
    RAG_MAX_CONTEXT_TOKENS: int = 3000
    RAG_MAX_RESULTS: int = 10

    # LLM configurations
    LLM_TEMPERATURE: float = 0.2
    LLM_TOP_P: float = 0.95
    LLM_MAX_OUTPUT_TOKENS: int = 1024
    LLM_RETRY_COUNT: int = 3
    LLM_TIMEOUT: int = 60
    LLM_STREAMING_ENABLED: bool = False

    # Pipeline configurations
    MAX_CONVERSATION_HISTORY: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @field_validator("GEMINI_API_KEY")
    @classmethod
    def check_gemini_key(cls, v: str) -> str:
        if not v or v.strip() == "" or v == "your_gemini_api_key_here":
            raise ValueError(
                "CRITICAL STARTUP CONFIGURATION ERROR: GEMINI_API_KEY is missing or contains the default value. "
                "Please configure GEMINI_API_KEY in your environment variables or .env file."
            )
        return v

    @field_validator("GROQ_API_KEY")
    @classmethod
    def check_groq_key(cls, v: str) -> str:
        if not v or v.strip() == "" or v == "your_groq_api_key_here":
            raise ValueError(
                "CRITICAL STARTUP CONFIGURATION ERROR: GROQ_API_KEY is missing or contains the default value. "
                "Please configure GROQ_API_KEY in your environment variables or .env file."
            )
        return v


try:
    settings = Settings()
except Exception as e:
    import sys
    print(f"\n{str(e)}\n", file=sys.stderr)
    sys.exit(1)
