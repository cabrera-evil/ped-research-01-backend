"""API integration tests for the hash table demo backend."""

import pytest
from fastapi.testclient import TestClient

from app.core.hash_table import HashTable
from app.main import app
from app.modules.inventory import service as inventory_service

API_KEY_HEADER = {"X-API-Key": "apikey"}


@pytest.fixture
def client() -> TestClient:
    # Reset in-memory storage before each test for deterministic behavior.
    inventory_service._inventory = HashTable()  # noqa: SLF001
    with TestClient(app) as test_client:
        yield test_client


def test_root_serves_html(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Hello, World!" in response.text


def test_health_check(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data


def test_ping_requires_api_key(client: TestClient) -> None:
    response = client.get("/api/v1/ping")
    assert response.status_code == 403


def test_ping_with_api_key(client: TestClient) -> None:
    response = client.get("/api/v1/ping", headers=API_KEY_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "pong"
    assert data["authenticated"] is True


def test_inventory_seeded_stats_show_collisions(client: TestClient) -> None:
    response = client.get("/api/v1/inventory/stats/hash")
    assert response.status_code == 200
    data = response.json()
    assert data["table_size"] == 10
    assert data["total_elements"] == 8
    assert data["cells_with_collision"] >= 2
    assert len(data["distribution"]) == data["table_size"]


def test_inventory_get_seeded_product(client: TestClient) -> None:
    response = client.get("/api/v1/inventory/P001")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "P001"
    assert data["name"] == "Laptop Stand"


def test_inventory_upsert_then_delete(client: TestClient) -> None:
    payload = {
        "code": "P999",
        "name": "Demo Product",
        "price": 10.5,
        "quantity": 9,
        "category": "Demo",
    }

    create_response = client.post("/api/v1/inventory/", json=payload)
    assert create_response.status_code == 200
    assert create_response.json()["code"] == "P999"

    payload["name"] = "Demo Product Updated"
    update_response = client.post("/api/v1/inventory/", json=payload)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Demo Product Updated"

    get_response = client.get("/api/v1/inventory/P999")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Demo Product Updated"

    delete_response = client.delete("/api/v1/inventory/P999")
    assert delete_response.status_code == 200

    not_found_response = client.get("/api/v1/inventory/P999")
    assert not_found_response.status_code == 404
