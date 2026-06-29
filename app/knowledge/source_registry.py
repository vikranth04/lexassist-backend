from typing import Dict, List, Optional
from datetime import datetime
from app.knowledge.source_metadata import BaseSourceMetadata
from app.knowledge.source_status import SourceStatus, SourceType


class SourceRegistry:
    """
    Manages in-memory registration, indexing, status state machine steps, and duplicate detection.
    """
    def __init__(self):
        self._sources: Dict[str, BaseSourceMetadata] = {}

    def register(self, source: BaseSourceMetadata):
        self._sources[source.source_id] = source

    def update_status(self, source_id: str, status: SourceStatus):
        if source_id in self._sources:
            self._sources[source_id].processing_status = status
            self._sources[source_id].last_updated = datetime.utcnow()

    def get(self, source_id: str) -> Optional[BaseSourceMetadata]:
        return self._sources.get(source_id)

    def remove(self, source_id: str) -> bool:
        if source_id in self._sources:
            del self._sources[source_id]
            return True
        return False

    def list_sources(self) -> List[BaseSourceMetadata]:
        return list(self._sources.values())

    def find_duplicate_website(self, url: str) -> Optional[BaseSourceMetadata]:
        for src in self._sources.values():
            if src.source_type == SourceType.WEBSITE:
                if getattr(src, "website_url", None) == url:
                    return src
        return None

    def find_duplicate_pdf(self, filename: str, file_size: int) -> Optional[BaseSourceMetadata]:
        for src in self._sources.values():
            if src.source_type == SourceType.PDF:
                if getattr(src, "filename", None) == filename and getattr(src, "file_size", None) == file_size:
                    return src
        return None
