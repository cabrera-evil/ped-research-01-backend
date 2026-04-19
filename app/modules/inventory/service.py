"""Business logic for inventory endpoints.

A single HashTable instance is created at module level to simulate
in-memory persistence across requests within a server session.
"""

from app.core.hash_table import HashTable
from app.modules.inventory.schemas import HashStatsResponse, ProductCreate, ProductResponse

# Module-level singleton — the only storage structure for the inventory.
_inventory: HashTable = HashTable()


def add_product(data: ProductCreate) -> ProductResponse:
    """Insert or update a product in the hash table."""
    _inventory.insert(data.code, data.model_dump())
    return ProductResponse(**data.model_dump())


def get_product(code: str) -> ProductResponse | None:
    """Return a product by code, or None if not found."""
    record = _inventory.search(code)
    if record is None:
        return None
    return ProductResponse(**record)


def delete_product(code: str) -> bool:
    """Remove a product. Returns True if it existed, False otherwise."""
    return _inventory.delete(code)


def list_products() -> list[ProductResponse]:
    """Return all products currently stored in the hash table."""
    return [ProductResponse(**v) for _, v in _inventory.list_all()]


def get_stats() -> HashStatsResponse:
    """Return internal hash table metrics."""
    return HashStatsResponse(**_inventory.stats())
