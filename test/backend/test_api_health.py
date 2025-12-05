"""
Test API Health Endpoints
Run with: python -m pytest test/backend/test_api_health.py -v
"""
import requests
import pytest

BASE_URL = "http://localhost:5646"


class TestHealthEndpoint:
    """Tests for the /health endpoint"""

    def test_health_endpoint_returns_200(self):
        """Test that health endpoint returns 200 status"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self):
        """Test that health endpoint returns valid JSON"""
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        assert "status" in data
        assert "message" in data

    def test_health_endpoint_message(self):
        """Test that health endpoint returns correct message"""
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        assert data["message"] == "API is live"
        assert data["status"] == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

