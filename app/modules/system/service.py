"""Business logic for system endpoints."""

from app.core.config import get_settings
from app.modules.system.schemas import HealthResponse, PingResponse


class SystemService:
    """Business logic for system endpoints."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def get_health_status(self) -> HealthResponse:
        return HealthResponse(
            status="healthy",
            version=self.settings.app_version,
            environment=self.settings.environment,
        )

    def get_ping(self) -> PingResponse:
        return PingResponse(message="pong", authenticated=True)
