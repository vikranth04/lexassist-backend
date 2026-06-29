import os
from typing import List
from urllib.parse import urlparse


class ValidationResult:
    def __init__(self, is_valid: bool, errors: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []


class SourceValidator:
    """
    Enforces validation checks for Website links and PDF documents.
    """
    def validate_website(self, url: str) -> ValidationResult:
        errors = []

        try:
            parsed = urlparse(url)

            if parsed.scheme not in ["http", "https"]:
                errors.append("Invalid URL scheme. Only HTTP and HTTPS are supported.")

            if not parsed.netloc:
                errors.append("Could not extract domain name from URL.")

            # Allow localhost during development
            if parsed.hostname in ["localhost", "127.0.0.1"]:
                return ValidationResult(is_valid=True)

            # Require HTTPS only for external websites
            if parsed.scheme != "https":
                errors.append("URL must use secure HTTPS protocol.")

        except Exception as e:
            errors.append(f"Malformatted URL expression: {str(e)}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors
        )

    def validate_pdf(self, filename: str, file_size: int) -> ValidationResult:
        errors = []
        if not filename.lower().endswith(".pdf"):
            errors.append("File must have a .pdf extension.")
        if file_size <= 0:
            errors.append("File size must be greater than 0.")
        if file_size > 15 * 1024 * 1024:
            errors.append("File size exceeds the maximum limit of 15 MB.")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
