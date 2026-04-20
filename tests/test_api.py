"""API integration tests for the hash table demo backend."""

from collections.abc import AsyncIterator

import httpx
import pytest

from app.core.hash_table import HashTable
from app.main import app
from app.modules.inventory import service as inventory_service
from app.modules.inventory.schemas import ProductCreate

pytestmark = pytest.mark.anyio
@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def seed_inventory() -> None:
    products = [
        ProductCreate(code="P001", name="Laptop Stand", price=39.99, quantity=15, category="Electronics"),
        ProductCreate(code="P010", name="USB Hub", price=24.99, quantity=30, category="Electronics"),
        ProductCreate(code="P002", name="Stapler", price=8.50, quantity=100, category="Office"),
        ProductCreate(code="P020", name="Tape Dispenser", price=5.99, quantity=80, category="Office"),
    ]
    for product in products:
        inventory_service.add_product(product)


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    inventory_service._inventory = HashTable()  # noqa: SLF001
    seed_inventory()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client


async def test_health_check(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data


async def test_inventory_seeded_stats_show_collisions(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/v1/inventory/stats/hash")
    assert response.status_code == 200
    data = response.json()
    assert data["table_size"] == 10
    assert data["total_elements"] == 4
    assert data["cells_with_collision"] == 2
    assert len(data["distribution"]) == data["table_size"]


async def test_inventory_get_seeded_product(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/v1/inventory/P001")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "P001"
    assert data["name"] == "Laptop Stand"


async def test_inventory_upsert_then_delete(client: httpx.AsyncClient) -> None:
    payload = {
        "code": "P999",
        "name": "Demo Product",
        "price": 10.5,
        "quantity": 9,
        "category": "Demo",
    }

    create_response = await client.post("/api/v1/inventory/", json=payload)
    assert create_response.status_code == 200
    assert create_response.json()["code"] == "P999"

    payload["name"] = "Demo Product Updated"
    update_response = await client.post("/api/v1/inventory/", json=payload)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Demo Product Updated"

    get_response = await client.get("/api/v1/inventory/P999")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Demo Product Updated"

    delete_response = await client.delete("/api/v1/inventory/P999")
    assert delete_response.status_code == 200

    not_found_response = await client.get("/api/v1/inventory/P999")
    assert not_found_response.status_code == 404
