from fastapi import APIRouter, Depends
import anyio
from app.schemas.website_schema import (
    WebsiteIndexRequest,
    WebsiteIndexResponse,
)
from app.knowledge.source_manager import SourceManager
from app.services.website_service import WebsiteService
from app.core.dependencies import get_source_manager, get_website_service
from app.core.exceptions import AppBaseException
from app.core.logger import logger

router = APIRouter()


async def handle_website_index(request: WebsiteIndexRequest, source_manager: SourceManager, website_service: WebsiteService):
    """
    Orchestrates the website indexing process.
    """
    url_str = str(request.url)
    logger.info(f"Website indexing request received for URL: {url_str}")

    try:
        # 1. Register website source ID
        logger.info(f"Registering website source for: {url_str}")
        source_id = await anyio.to_thread.run_sync(
            source_manager.register_website, url_str
        )

        # 2. Run crawl and execute full RAG pipeline
        logger.info(f"Starting website crawling and indexing pipeline for: {url_str}")
        result = await anyio.to_thread.run_sync(
            website_service.index_website, url_str, source_id
        )

        logger.info(f"Website indexing completed for: {url_str}. "
                    f"Pages: {result.get('pages_crawled', 0)}, "
                    f"Chunks: {result.get('chunks_created', 0)}, "
                    f"Vectors: {result.get('vectors_indexed', 0)}")

        return result

    except Exception as e:
        logger.error(f"Failed to index website {url_str}: {str(e)}")
        if isinstance(e, AppBaseException):
            raise e
        raise AppBaseException(message=str(e), status_code=500)


@router.post(
    "/website/index",
    response_model=WebsiteIndexResponse,
    summary="Index Website",
    description="Index a website URL by registering, crawling, chunking, and embedding its contents into ChromaDB."
)
async def index_website(
    request: WebsiteIndexRequest,
    source_manager: SourceManager = Depends(get_source_manager),
    website_service: WebsiteService = Depends(get_website_service)
):
    return await handle_website_index(request, source_manager, website_service)


@router.post(
    "/index-website",
    response_model=WebsiteIndexResponse,
    summary="Index Website (Legacy)",
    description="Index a website URL by registering and crawling its contents.",
    deprecated=True
)
async def index_website_legacy(
    request: WebsiteIndexRequest,
    source_manager: SourceManager = Depends(get_source_manager),
    website_service: WebsiteService = Depends(get_website_service)
):
    return await handle_website_index(request, source_manager, website_service)
