"""HTTP layer for inventory endpoints."""

from fastapi import HTTPException, status

from app.modules.inventory import service
from app.modules.inventory.schemas import HashStatsResponse, ProductCreate, ProductResponse


class InventoryController:
    """HTTP layer — validates business rules and delegates to service functions."""

    async def add_product(self, data: ProductCreate) -> ProductResponse:
        return service.add_product(data)

    async def get_product(self, code: str) -> ProductResponse:
        product = service.get_product(code)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product '{code}' not found.",
            )
        return product

    async def delete_product(self, code: str) -> dict[str, str]:
        removed = service.delete_product(code)
        if not removed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product '{code}' not found.",
            )
        return {"message": f"Product '{code}' deleted."}

    async def list_products(self) -> list[ProductResponse]:
        return service.list_products()

    async def get_stats(self) -> HashStatsResponse:
        return service.get_stats()
