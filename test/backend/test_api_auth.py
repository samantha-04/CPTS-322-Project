"""
Test Authentication API Endpoints
Run with: python -m pytest test/backend/test_api_auth.py -v
"""
import requests
import pytest
import uuid

BASE_URL = "http://localhost:5646"


class TestRegistrationEndpoint:
    """Tests for the /api/auth/register endpoint"""

    def test_register_new_user(self):
        """Test registering a new user"""
        unique_email = f"test_{uuid.uuid4().hex[:8]}@test.com"
        response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": unique_email,
            "password": "testpassword123",
            "name": "Test User"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert "user" in data
        assert data["user"]["email"] == unique_email.lower()

    def test_register_missing_email(self):
        """Test registration fails without email"""
        response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "password": "testpassword123"
        })
        assert response.status_code == 400
        data = response.json()
        assert "Email is required" in data["message"]

    def test_register_missing_password(self):
        """Test registration fails without password"""
        response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": "test@test.com"
        })
        assert response.status_code == 400
        data = response.json()
        assert "Password is required" in data["message"]

    def test_register_short_password(self):
        """Test registration fails with short password"""
        unique_email = f"test_{uuid.uuid4().hex[:8]}@test.com"
        response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": unique_email,
            "password": "short"
        })
        assert response.status_code == 400
        data = response.json()
        assert "at least 8 characters" in data["message"]

    def test_register_duplicate_user(self):
        """Test registration fails for existing user"""
        # Try to register with a known demo user
        response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": "alice@wsu.edu",
            "password": "testpassword123"
        })
        assert response.status_code == 409
        data = response.json()
        assert "already exists" in data["message"]


class TestLoginEndpoint:
    """Tests for the /api/auth/login endpoint"""

    def test_login_valid_credentials(self):
        """Test login with valid demo account"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "alice@wsu.edu",
            "password": "123"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert "user" in data
        assert data["user"]["email"] == "alice@wsu.edu"

    def test_login_invalid_password(self):
        """Test login fails with wrong password"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "alice@wsu.edu",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        data = response.json()
        assert "Invalid credentials" in data["message"]

    def test_login_nonexistent_user(self):
        """Test login fails for non-existent user"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "nonexistent@test.com",
            "password": "testpassword123"
        })
        assert response.status_code == 401
        data = response.json()
        assert "Invalid credentials" in data["message"]

    def test_login_missing_email(self):
        """Test login fails without email"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "password": "testpassword123"
        })
        assert response.status_code == 400

    def test_login_missing_password(self):
        """Test login fails without password"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "alice@wsu.edu"
        })
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

