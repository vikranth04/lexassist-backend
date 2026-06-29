import math
from typing import List, Dict, Any
from app.core.exceptions import VectorValidationException


class VectorValidator:
    """
    Validates vectors and metadata structure parameters prior to database execution.
    """
    def __init__(self, expected_dimension: int = 768):
        self.expected_dimension = expected_dimension

    def validate_vector(self, vector_id: str, embedding: List[float], metadata: Dict[str, Any]) -> bool:
        """Validates ID, embedding values, and metadata properties. Raises VectorValidationException."""
        if not vector_id or not vector_id.strip():
            raise VectorValidationException("Vector ID cannot be empty.")
        if not embedding:
            raise VectorValidationException("Embedding list cannot be empty.")
        if len(embedding) != self.expected_dimension:
            raise VectorValidationException(
                f"Dimension size check failed. Expected {self.expected_dimension}, got {len(embedding)}."
            )

        for val in embedding:
            if math.isnan(val) or math.isinf(val):
                raise VectorValidationException("Vector content contains invalid NaN or Infinite values.")

        if not metadata:
            raise VectorValidationException("Metadata descriptor cannot be empty.")

        return True
