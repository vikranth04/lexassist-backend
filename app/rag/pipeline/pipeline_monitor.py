from typing import Dict, Any, List
from app.core.logger import logger

class PipelineMonitor:
    """
    Monitors pipeline execution health and success rates.
    """

    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.error_counts: Dict[str, int] = {}

    def log_request(self):
        self.total_requests += 1

    def log_success(self):
        self.successful_requests += 1

    def log_error(self, error_type: str):
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        logger.error(f"Pipeline error monitored: {error_type}")

    def get_health_stats(self) -> Dict[str, Any]:
        """Returns diagnostic information about the pipeline."""
        success_rate = (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 100
        return {
            "total_requests": self.total_requests,
            "success_rate": f"{success_rate:.2f}%",
            "errors": self.error_counts
        }
