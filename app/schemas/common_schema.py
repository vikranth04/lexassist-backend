from pydantic import BaseModel
from typing import Any, Optional, List


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "Request completed successfully."


class ErrorResponse(BaseModel):
    success: bool = False
    error: str


class PaginationResponse(BaseModel):
    page: int
    size: int
    total: int
    pages: int


class APIResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None


class MessageResponse(BaseModel):
    role: str
    content: str
