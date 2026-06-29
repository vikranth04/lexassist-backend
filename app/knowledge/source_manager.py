from app.knowledge.source_status import SourceStatus
from app.knowledge.source_validator import SourceValidator
from app.knowledge.source_factory import SourceFactory
from app.knowledge.source_registry import SourceRegistry
from app.repositories.source_repository import SourceRepository
from app.core.exceptions import (
    SourceValidationException,
    DuplicateSourceException,
    RegistrationException
)
from app.core.logger import logger


class SourceManager:
    """
    Drives the knowledge source lifecycle from initial submission to validation, registration, and persistence.
    """
    def __init__(self, registry: SourceRegistry, repo: SourceRepository):
        self.validator = SourceValidator()
        self.factory = SourceFactory()
        self.registry = registry
        self.repo = repo

    def register_website(self, url: str) -> str:
        """Runs the website source registration lifecycle steps and returns unique Source ID."""
        logger.info(f"Submitting website source registration request: {url}")

        # Validate URL parameters
        validation = self.validator.validate_website(url)
        if not validation.is_valid:
            errors_msg = ", ".join(validation.errors)
            logger.warning(f"Website source validation failed: {errors_msg}")
            raise SourceValidationException(errors_msg)

        # Check duplication
        duplicate = self.registry.find_duplicate_website(url)
        if duplicate:
            logger.warning(f"Duplicate website registration request: {url}")
            raise DuplicateSourceException(
                f"Website URL '{url}' is already registered as source ID: {duplicate.source_id}"
            )

        # Create metadata shape
        source_meta = self.factory.create_website_source(url)
        logger.info(f"Generated source ID: {source_meta.source_id} for URL: {url}")

        # Register and Persist details
        self.registry.register(source_meta)
        self.repo.save(source_meta)

        # Mark source registered
        self.registry.update_status(source_meta.source_id, SourceStatus.REGISTERED)
        self.repo.update_status(source_meta.source_id, SourceStatus.REGISTERED)

        logger.info(f"Source registration workflow completed successfully: {source_meta.source_id}")
        return source_meta.source_id

    def register_pdf(self, filename: str, file_size: int, storage_path: str) -> str:
        """Runs the PDF source registration lifecycle steps and returns unique Source ID."""
        logger.info(f"Submitting PDF source registration request: {filename}")

        # Validate PDF parameters
        validation = self.validator.validate_pdf(filename, file_size)
        if not validation.is_valid:
            errors_msg = ", ".join(validation.errors)
            logger.warning(f"PDF source validation failed: {errors_msg}")
            raise SourceValidationException(errors_msg)

        # Check duplication
        duplicate = self.registry.find_duplicate_pdf(filename, file_size)
        if duplicate:
            logger.warning(f"Duplicate PDF registration request: {filename}")
            raise DuplicateSourceException(
                f"PDF file '{filename}' with size {file_size} is already registered as source ID: {duplicate.source_id}"
            )

        # Create metadata shape
        source_meta = self.factory.create_pdf_source(filename, file_size, storage_path)
        logger.info(f"Generated source ID: {source_meta.source_id} for File: {filename}")

        # Register and Persist details
        self.registry.register(source_meta)
        self.repo.save(source_meta)

        # Mark source registered
        self.registry.update_status(source_meta.source_id, SourceStatus.REGISTERED)
        self.repo.update_status(source_meta.source_id, SourceStatus.REGISTERED)

        logger.info(f"Source registration workflow completed successfully: {source_meta.source_id}")
        return source_meta.source_id
