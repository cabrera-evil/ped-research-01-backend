"""API endpoint tests for the template."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
API_KEY_HEADER = {"X-API-Key": "apikey"}


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data


def test_ping_requires_api_key() -> None:
    response = client.get("/api/v1/ping")
    assert response.status_code == 403


def test_ping_with_api_key() -> None:
    response = client.get("/api/v1/ping", headers=API_KEY_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "pong"
    assert data["authenticated"] is True
