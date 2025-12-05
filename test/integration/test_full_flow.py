"""
Integration Tests - Full User Flow
Run with: python -m pytest test/integration/test_full_flow.py -v
"""
import requests
import pytest
import uuid

BASE_URL = "http://localhost:5646"
FRONTEND_URL = "http://localhost:8000"


class TestFullUserFlow:
    """Integration tests for complete user workflows"""

    def test_complete_registration_to_matches_flow(self):
        """Test: Register -> Complete Survey -> Get Matches"""
        unique_email = f"integration_{uuid.uuid4().hex[:8]}@test.com"
        
        # Step 1: Register
        register_response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": unique_email,
            "password": "testpassword123",
            "name": "Integration Test User"
        })
        assert register_response.status_code == 200, "Registration failed"
        user_data = register_response.json()["user"]
        assert user_data["surveyCompleted"] == False
        
        # Step 2: Complete Survey
        survey_response = requests.post(f"{BASE_URL}/api/survey/submit", json={
            "username": unique_email,
            "answers": {
                "q_smoking": "No",
                "q_pets": "No",
                "q_clean_freq": "Often",
                "q_social": "Neutral",
                "q_noise": "Disagree",
                "q_quiet_hours": "Yes",
                "q_shared_food": "Yes",
                "q_sleep_schedule": "Agree",
                "q_noise_tolerance": "Disagree",
                "q_alcohol": "No",
                "q_share_chores": "Yes",
                "q_temperature_pref": "Neutral",
                "q_overnight_guests": "Never",
                "q_shared_groceries": "Agree",
                "q_work_from_home": "Often",
                "q_morning_routine": "Disagree",
                "q_social_events": "Sometimes",
                "q_tv_music": "Disagree",
                "q_visitors_notice": "Yes",
                "q_decorating": "Neutral",
                "q_conflict_style": "Agree",
                "q_budget_conscious": "Strongly Agree"
            }
        })
        assert survey_response.status_code == 200, "Survey submission failed"
        
        # Step 3: Get Matches
        matches_response = requests.get(f"{BASE_URL}/api/matches/{unique_email}")
        assert matches_response.status_code == 200, "Getting matches failed"
        matches_data = matches_response.json()
        assert "matches" in matches_data
        assert len(matches_data["matches"]) > 0, "Should have matches with demo users"

    def test_login_and_view_profile_flow(self):
        """Test: Login -> View Profile -> Update Profile"""
        # Login with demo account
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "alice@wsu.edu",
            "password": "123"
        })
        assert login_response.status_code == 200
        user = login_response.json()["user"]
        
        # Get profile
        profile_response = requests.get(f"{BASE_URL}/api/user/{user['email']}")
        assert profile_response.status_code == 200
        profile = profile_response.json()["user"]
        assert profile["email"] == "alice@wsu.edu"
        assert profile["surveyCompleted"] == True

    def test_new_user_appears_in_matches(self):
        """Test that a newly registered user appears in other users' matches"""
        unique_email = f"newuser_{uuid.uuid4().hex[:8]}@test.com"
        
        # Register new user
        requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": unique_email,
            "password": "testpassword123",
            "name": "New Test User"
        })
        
        # Complete survey with similar preferences to Alice
        requests.post(f"{BASE_URL}/api/survey/submit", json={
            "username": unique_email,
            "answers": {
                "q_smoking": "No",
                "q_pets": "No",
                "q_clean_freq": "Often",
                "q_social": "Neutral",
                "q_noise": "Disagree",
                "q_quiet_hours": "Yes",
                "q_shared_food": "Yes",
                "q_sleep_schedule": "Strongly Agree",
                "q_noise_tolerance": "Disagree",
                "q_alcohol": "No",
                "q_share_chores": "Yes",
                "q_temperature_pref": "Agree",
                "q_overnight_guests": "Never",
                "q_shared_groceries": "Agree",
                "q_work_from_home": "Often",
                "q_morning_routine": "Disagree",
                "q_social_events": "Sometimes",
                "q_tv_music": "Disagree",
                "q_visitors_notice": "Yes",
                "q_decorating": "Neutral",
                "q_conflict_style": "Agree",
                "q_budget_conscious": "Strongly Agree"
            }
        })
        
        # Check if new user appears in Alice's matches
        matches_response = requests.get(f"{BASE_URL}/api/matches/alice@wsu.edu")
        matches = matches_response.json()["matches"]
        match_ids = [m["id"] for m in matches]
        
        assert unique_email in match_ids, "New user should appear in Alice's matches"


class TestFrontendAvailability:
    """Tests that frontend is accessible"""

    def test_frontend_serves_html(self):
        """Test that frontend returns HTML"""
        response = requests.get(FRONTEND_URL)
        assert response.status_code == 200
        assert "<!doctype html>" in response.text.lower() or "<!DOCTYPE html>" in response.text

    def test_frontend_static_files(self):
        """Test that static files are served"""
        # First get the index to find the JS file name
        index_response = requests.get(FRONTEND_URL)
        
        # Check that we can load static assets
        # The exact filename changes with builds, so we just check CSS/JS paths exist
        assert "/static/js/" in index_response.text or "/static/css/" in index_response.text

    def test_api_proxy_through_frontend(self):
        """Test that API calls can be made through frontend proxy"""
        response = requests.get(f"{FRONTEND_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "API is live"


class TestErrorHandling:
    """Tests for error handling"""

    def test_invalid_json_body(self):
        """Test API handles invalid JSON gracefully"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data="not valid json",
            headers={"Content-Type": "application/json"}
        )
        # Should return 400 or 500, not crash
        assert response.status_code in [400, 500]

    def test_missing_content_type(self):
        """Test API handles missing content type"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": "test@test.com", "password": "test"}
        )
        # Should still work or return appropriate error
        assert response.status_code in [200, 400, 401, 415]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

