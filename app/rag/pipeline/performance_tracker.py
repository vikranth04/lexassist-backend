import time
from typing import Dict, Any, List
from app.core.logger import logger

class PerformanceTracker:
    """
    Collects latency and usage metrics for pipeline stages.
    """

    def __init__(self):
        self.metrics: Dict[str, float] = {}
        self._start_times: Dict[str, float] = {}

    def start_stage(self, stage_name: str):
        """Marks the start of a stage."""
        self._start_times[stage_name] = time.time()

    def end_stage(self, stage_name: str):
        """Marks the end of a stage and calculates duration."""
        if stage_name in self._start_times:
            duration = time.time() - self._start_times[stage_name]
            self.metrics[stage_name] = duration
            logger.info(f"Stage '{stage_name}' completed in {duration:.4f}s")

    def get_metrics(self) -> Dict[str, float]:
        """Returns all collected duration metrics."""
        return self.metrics

    def get_total_latency(self) -> float:
        """Calculates total latency based on individual stages."""
        return sum(self.metrics.values())
