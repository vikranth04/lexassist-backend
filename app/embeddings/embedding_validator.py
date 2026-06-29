import math
from typing import List
from app.core.exceptions import EmbeddingValidationException


class EmbeddingValidator:
    """
    Validates output vector traits: dimension match, NaN/Inf check, and empty sets.
    """
    def __init__(self, expected_dimension: int = 768):
        self.expected_dimension = expected_dimension

    def validate(self, vector: List[float]) -> bool:
        """Verifies vector structure. Raises EmbeddingValidationException on failure."""
        if not vector:
            raise EmbeddingValidationException("Generated vector is empty.")
        if len(vector) != self.expected_dimension:
            raise EmbeddingValidationException(
                f"Generated vector dimension mismatch. Expected {self.expected_dimension}, got {len(vector)}."
            )
        # NaN / Inf validation check
        for element in vector:
            if math.isnan(element) or math.isinf(element):
                raise EmbeddingValidationException("Vector contains invalid elements (NaN or Inf values).")

        return True
