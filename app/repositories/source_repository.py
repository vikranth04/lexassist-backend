from typing import Dict, Optional
from datetime import datetime
from app.knowledge.source_metadata import BaseSourceMetadata
from app.knowledge.source_status import SourceStatus


class SourceRepository:
    """
    Handles data persistence for registered knowledge sources.
    Uses an in-memory repository structure as a developer database fallback.
    """
    def __init__(self):
        self._sources: Dict[str, BaseSourceMetadata] = {}

    def save(self, source: BaseSourceMetadata):
        """Saves or updates a knowledge source metadata entry."""
        self._sources[source.source_id] = source

    def get(self, source_id: str) -> Optional[BaseSourceMetadata]:
        """Retrieves metadata for a knowledge source by ID."""
        return self._sources.get(source_id)

    def delete(self, source_id: str) -> bool:
        """Removes a knowledge source metadata entry by ID."""
        if source_id in self._sources:
            del self._sources[source_id]
            return True
        return False

    def update_status(self, source_id: str, status: SourceStatus):
        """Updates the processing status of a knowledge source."""
        if source_id in self._sources:
            self._sources[source_id].processing_status = status
            self._sources[source_id].last_updated = datetime.utcnow()
