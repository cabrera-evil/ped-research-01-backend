"""Inventory routes.

IMPORTANT: /stats/hash is registered before /{code} to prevent
FastAPI from treating the literal string "stats" as a path parameter.
"""

from fastapi import APIRouter

from app.modules.inventory.controller import InventoryController
from app.modules.inventory.schemas import HashStatsResponse, ProductCreate, ProductResponse
from app.shared.schemas import ErrorResponse

controller = InventoryController()
public_router = APIRouter()


@public_router.post(
    "/",
    response_model=ProductResponse,
    tags=["Inventory (Hash Table)"],
    summary="Add or update a product",
)
async def add_product(data: ProductCreate) -> ProductResponse:
    return await controller.add_product(data)


@public_router.get(
    "/",
    response_model=list[ProductResponse],
    tags=["Inventory (Hash Table)"],
    summary="List all products",
)
async def list_products() -> list[ProductResponse]:
    return await controller.list_products()


# Must be defined BEFORE /{code} to avoid route shadowing
@public_router.get(
    "/stats/hash",
    response_model=HashStatsResponse,
    tags=["Inventory (Hash Table)"],
    summary="Get hash table internal stats",
)
async def get_stats() -> HashStatsResponse:
    return await controller.get_stats()


@public_router.get(
    "/{code}",
    response_model=ProductResponse,
    responses={404: {"model": ErrorResponse}},
    tags=["Inventory (Hash Table)"],
    summary="Get product by code",
)
async def get_product(code: str) -> ProductResponse:
    return await controller.get_product(code)


@public_router.delete(
    "/{code}",
    responses={404: {"model": ErrorResponse}},
    tags=["Inventory (Hash Table)"],
    summary="Delete product by code",
)
async def delete_product(code: str) -> dict[str, str]:
    return await controller.delete_product(code)
