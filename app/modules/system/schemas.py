"""System module schemas."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Health check response schema."""

    model_config = ConfigDict(protected_namespaces=())

    status: Literal["healthy"]
    version: str
    environment: str


class PingResponse(BaseModel):
    """Protected sample endpoint response schema."""

    message: str
    authenticated: bool
