from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional
from app.knowledge.source_status import SourceStatus, SourceType


class BaseSourceMetadata(BaseModel):
    source_id: str
    source_type: SourceType
    submitted_time: datetime
    last_updated: datetime
    processing_status: SourceStatus


class WebsiteMetadata(BaseSourceMetadata):
    website_url: str
    domain: str
    title: Optional[str] = None


class PDFMetadata(BaseSourceMetadata):
    filename: str
    file_size: int
    file_type: str = "application/pdf"
    storage_path: str
