from pydantic import BaseModel
from typing import Optional


class SourceAttribution(BaseModel):
    source_title: str
    source_type: str
    website_url: Optional[str] = None
    page_number: int = 1
    chunk_id: str
    confidence_score: float = 1.0
