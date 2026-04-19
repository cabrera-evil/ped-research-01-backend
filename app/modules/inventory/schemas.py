"""Inventory module schemas."""

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    """Schema for creating or updating a product."""

    model_config = ConfigDict(protected_namespaces=())

    code: str  # Hash key — e.g. "P001"
    name: str
    price: float
    quantity: int
    category: str


class ProductResponse(ProductCreate):
    """Schema returned for a single product."""

    pass


class HashStatsResponse(BaseModel):
    """Internal hash table metrics."""

    model_config = ConfigDict(protected_namespaces=())

    table_size: int
    total_elements: int
    used_cells: int
    cells_with_collision: int
    load_factor: float
    distribution: list[int]
