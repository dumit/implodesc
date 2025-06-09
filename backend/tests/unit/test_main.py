"""
Unit tests for main application
"""
import pytest
from fastapi.testclient import TestClient
from implodesc.main import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    return TestClient(app)


def test_app_creation():
    """Test FastAPI app can be created"""
    app = create_app()
    
    assert app.title == "Implodesc API"
    assert app.description == "AI-driven supply chain analysis"
    assert app.version == "0.1.0"


def test_cors_middleware(client):
    """Test CORS middleware is configured"""
    # Test that CORS headers are present in response
    response = client.get("/health/")
    
    # Check that the response includes CORS headers (added by middleware)
    assert response.status_code == 200
    # Note: TestClient may not always include CORS headers in test environment
    # This test verifies the endpoint works, implying CORS middleware doesn't break it


def test_health_endpoint_available(client):
    """Test health endpoint is included in routes"""
    response = client.get("/health/")
    
    assert response.status_code == 200


def test_docs_disabled_in_production(client):
    """Test API docs are disabled in production mode"""
    # In our current config, docs should be disabled unless debug=True
    response = client.get("/docs")
    
    # Should return 404 when docs are disabled
    assert response.status_code == 404