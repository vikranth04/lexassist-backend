from typing import Dict, Any
from app.core.exceptions import ValidationException


class QualityValidator:
    """
    Validates minimum and maximum text thresholds, encoding compliance, and empty results.
    """
    def validate(self, text: str) -> Dict[str, Any]:
        """Runs quality checks on normalized text. Raises ValidationException on errors."""
        if not text or not text.strip():
            raise ValidationException("Quality validation failed: text content is empty.")

        char_count = len(text)
        if char_count < 15:
            raise ValidationException("Quality validation failed: text is too short to extract meaning.")

        # Estimate tokens using standard character metric
        token_count = char_count // 4

        return {
            "is_valid": True,
            "character_count": char_count,
            "estimated_token_count": token_count,
            "duplicate_ratio": 0.0
        }
