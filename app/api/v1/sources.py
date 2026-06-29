from fastapi import APIRouter, Depends
from typing import List
from app.core.dependencies import get_source_service
from app.services.source_service import SourceService
from app.schemas.source_schema import SourceAttribution

router = APIRouter()


@router.get(
    "/sources",
    response_model=List[SourceAttribution],
    summary="Get Sources & Citations",
    description="Retrieves a list of indexed legal document and website reference sources."
)
async def get_sources(
    service: SourceService = Depends(get_source_service)
):
    """
    Returns unique sources metadata including title, type, url, page, and chunk id.
    """
    return service.get_formatted_sources()
