"""HTTP layer for system endpoints."""

from app.modules.system.schemas import HealthResponse, PingResponse
from app.modules.system.service import SystemService


class SystemController:
    """HTTP layer for system endpoints."""

    def __init__(self) -> None:
        self.service = SystemService()

    async def health_check(self) -> HealthResponse:
        return self.service.get_health_status()

    async def ping(self) -> PingResponse:
        return self.service.get_ping()
