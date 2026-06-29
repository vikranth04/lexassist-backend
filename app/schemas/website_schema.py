from pydantic import BaseModel, HttpUrl


class WebsiteIndexRequest(BaseModel):
    url: HttpUrl


class WebsiteIndexResponse(BaseModel):
    success: bool
    message: str
    website: str
    pages_crawled: int = 1
    chunks_created: int = 0
    vectors_indexed: int = 0
    processing_time: str = "0.0 seconds"
