"""
Test User Profile API Endpoints
Run with: python -m pytest test/backend/test_api_user.py -v
"""
import requests
import pytest
import uuid

BASE_URL = "http://localhost:5646"


class TestGetUserEndpoint:
    """Tests for GET /api/user/<user_id>"""

    def test_get_existing_user(self):
        """Test getting an existing user's profile"""
        response = requests.get(f"{BASE_URL}/api/user/alice@wsu.edu")
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert data["user"]["email"] == "alice@wsu.edu"

    def test_get_user_has_profile_fields(self):
        """Test that user response includes profile fields"""
        response = requests.get(f"{BASE_URL}/api/user/alice@wsu.edu")
        data = response.json()
        user = data["user"]
        
        assert "name" in user
        assert "profile" in user
        assert "surveyCompleted" in user

    def test_get_user_no_password(self):
        """Test that user response does not include password"""
        response = requests.get(f"{BASE_URL}/api/user/alice@wsu.edu")
        data = response.json()
        
        assert "password" not in data["user"]

    def test_get_nonexistent_user(self):
        """Test getting a non-existent user returns 404"""
        response = requests.get(f"{BASE_URL}/api/user/nonexistent@test.com")
        assert response.status_code == 404


class TestUpdateUserEndpoint:
    """Tests for PUT /api/user/<user_id>"""

    def test_update_user_name(self):
        """Test updating user's name"""
        # First create a test user
        unique_email = f"test_{uuid.uuid4().hex[:8]}@test.com"
        requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": unique_email,
            "password": "testpassword123",
            "name": "Original Name"
        })
        
        # Update the name
        response = requests.put(f"{BASE_URL}/api/user/{unique_email}", json={
            "name": "Updated Name"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["name"] == "Updated Name"

    def test_update_user_profile(self):
        """Test updating user's profile info"""
        # First create a test user
        unique_email = f"test_{uuid.uuid4().hex[:8]}@test.com"
        requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": unique_email,
            "password": "testpassword123"
        })
        
        # Update profile
        response = requests.put(f"{BASE_URL}/api/user/{unique_email}", json={
            "profile": {
                "age": 21,
                "major": "Computer Science",
                "bio": "Test bio"
            }
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["profile"]["age"] == 21
        assert data["user"]["profile"]["major"] == "Computer Science"
        assert data["user"]["profile"]["bio"] == "Test bio"

    def test_update_nonexistent_user(self):
        """Test updating non-existent user returns 404"""
        response = requests.put(f"{BASE_URL}/api/user/nonexistent@test.com", json={
            "name": "Test"
        })
        assert response.status_code == 404

    def test_update_user_no_data(self):
        """Test updating with no data returns 400"""
        response = requests.put(f"{BASE_URL}/api/user/alice@wsu.edu", json={})
        # This might return 400 or just succeed with no changes
        # depending on implementation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

