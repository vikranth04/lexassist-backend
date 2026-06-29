import uuid
from datetime import datetime
from urllib.parse import urlparse
from app.knowledge.source_status import SourceStatus, SourceType
from app.knowledge.source_metadata import WebsiteMetadata, PDFMetadata


class SourceFactory:
    """
    Instantiates validated metadata objects with collision-resistant SRC_ prefixed identifiers.
    """
    def create_website_source(self, url: str) -> WebsiteMetadata:
        # Generate predictable, unique ID
        unique_suffix = uuid.uuid4().hex[:8].upper()
        source_id = f"SRC_WEB_{unique_suffix}"
        domain = urlparse(url).netloc
        now = datetime.utcnow()

        return WebsiteMetadata(
            source_id=source_id,
            source_type=SourceType.WEBSITE,
            submitted_time=now,
            last_updated=now,
            processing_status=SourceStatus.PENDING,
            website_url=url,
            domain=domain,
            title=None
        )

    def create_pdf_source(self, filename: str, file_size: int, storage_path: str) -> PDFMetadata:
        unique_suffix = uuid.uuid4().hex[:8].upper()
        source_id = f"SRC_PDF_{unique_suffix}"
        now = datetime.utcnow()

        return PDFMetadata(
            source_id=source_id,
            source_type=SourceType.PDF,
            submitted_time=now,
            last_updated=now,
            processing_status=SourceStatus.PENDING,
            filename=filename,
            file_size=file_size,
            storage_path=storage_path
        )
