import time
from collections import defaultdict
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    In-memory rate limiter middleware that tracks client IPs and rejects requests exceeding limits.
    """
    def __init__(self, app, rate_limit_seconds: int = 60, max_requests: int = 100):
        super().__init__(app)
        self.rate_limit_seconds = rate_limit_seconds
        self.max_requests = max_requests
        self._request_history = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Prune older timestamps
        self._request_history[client_ip] = [
            t for t in self._request_history[client_ip]
            if now - t < self.rate_limit_seconds
        ]

        if len(self._request_history[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": {
                        "code": "TooManyRequests",
                        "message": "Rate limit exceeded. Please try again later.",
                        "details": None
                    }
                }
            )

        self._request_history[client_ip].append(now)
        return await call_next(request)
