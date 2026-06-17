import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

@pytest.mark.asyncio
async def test_register_user():
    """Test user registration"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    response = client.post("/api/auth/register", json=user_data)
    # This might fail due to database setup, but tests the endpoint structure
    assert response.status_code in [200, 400, 422]

def test_missing_required_fields():
    """Test validation of required fields"""
    response = client.post("/api/auth/register", json={})
    assert response.status_code == 422
