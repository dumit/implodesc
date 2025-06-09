"""
Unit tests for health check endpoints
"""
import pytest
from fastapi.testclient import TestClient
from implodesc.main import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    return TestClient(app)


def test_health_check(client):
    """Test basic health check endpoint"""
    response = client.get("/health/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"
    assert "timestamp" in data


def test_readiness_check(client):
    """Test readiness check endpoint"""
    response = client.get("/health/ready")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["version"] == "0.1.0"
    assert "timestamp" in data
    assert "dependencies" in data
    assert "database" in data["dependencies"]
    assert "redis" in data["dependencies"]
    assert "ai_service" in data["dependencies"]


def test_liveness_check(client):
    """Test liveness check endpoint"""
    response = client.get("/health/live")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data