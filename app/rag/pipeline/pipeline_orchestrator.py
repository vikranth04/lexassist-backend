import time
import inspect
import anyio
from typing import Dict, Any, Optional
from app.core.logger import logger
from app.core.exceptions import AppBaseException, GroqConnectionException
from app.rag.pipeline.performance_tracker import PerformanceTracker

class PipelineOrchestrator:
    """
    Orchestrates the workflow of the RAG pipeline.

    Responsibilities:
    - Sequence component execution
    - Handle retries for specific stages
    - Manage execution timing and logging
    """

    def __init__(self, performance_tracker: Optional[PerformanceTracker] = None):
        self.tracker = performance_tracker or PerformanceTracker()

    async def execute_stage(self, stage_name: str, func, *args, **kwargs):
        """
        Executes a pipeline stage with monitoring and optional retry logic.
        Supports both synchronous and asynchronous functions.
        """
        self.tracker.start_stage(stage_name)
        # Only retry critical network-dependent stages
        max_retries = 2 if stage_name in ["groq_generation", "query_embedding", "vector_search"] else 1

        last_error = None
        for attempt in range(max_retries):
            try:
                # Intelligently handle sync vs async function calls
                if inspect.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                self.tracker.end_stage(stage_name)
                return result
            except Exception as e:
                last_error = e
                logger.warning(f"Stage '{stage_name}' failed (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    await anyio.sleep(1) # Async-friendly sleep

        self.tracker.end_stage(stage_name)
        raise last_error
