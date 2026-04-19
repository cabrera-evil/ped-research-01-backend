"""System routes for health and sample protected endpoints."""

from fastapi import APIRouter

from app.modules.system.controller import SystemController
from app.modules.system.schemas import HealthResponse, PingResponse
from app.shared.schemas import ErrorResponse

controller = SystemController()
public_router = APIRouter()
protected_router = APIRouter()


@public_router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check() -> HealthResponse:
    return await controller.health_check()


@protected_router.get(
    "/ping",
    response_model=PingResponse,
    responses={403: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    tags=["System"],
)
async def ping() -> PingResponse:
    return await controller.ping()
