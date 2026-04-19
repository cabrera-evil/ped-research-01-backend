"""Shared schemas used across multiple modules."""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str
    detail: str | None = None
