from enum import Enum


class SourceStatus(str, Enum):
    PENDING = "PENDING"
    VALIDATING = "VALIDATING"
    REGISTERED = "REGISTERED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"


class SourceType(str, Enum):
    WEBSITE = "WEBSITE"
    PDF = "PDF"
    DOCX = "DOCX"
    TXT = "TXT"
    MARKDOWN = "MARKDOWN"
    DATABASE = "DATABASE"
    API = "API"
    CLOUD_STORAGE = "CLOUD_STORAGE"
