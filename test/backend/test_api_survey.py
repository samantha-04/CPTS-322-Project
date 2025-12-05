"""
Test Survey API Endpoint
Run with: python -m pytest test/backend/test_api_survey.py -v
"""
import requests
import pytest
import uuid

BASE_URL = "http://localhost:5646"


class TestSurveySubmitEndpoint:
    """Tests for the /api/survey/submit endpoint"""

    def test_submit_survey_success(self):
        """Test submitting a valid survey"""
        unique_user = f"test_{uuid.uuid4().hex[:8]}@test.com"
        
        # First register the user
        requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": unique_user,
            "password": "testpassword123"
        })
        
        # Submit survey
        response = requests.post(f"{BASE_URL}/api/survey/submit", json={
            "username": unique_user,
            "answers": {
                "q_smoking": "No",
                "q_pets": "Yes",
                "q_clean_freq": "Often",
                "q_social": "Agree",
                "q_noise": "Neutral",
                "q_quiet_hours": "Yes",
                "q_shared_food": "Yes",
                "q_sleep_schedule": "Agree",
                "q_noise_tolerance": "Neutral",
                "q_alcohol": "No",
                "q_share_chores": "Yes",
                "q_temperature_pref": "Neutral",
                "q_overnight_guests": "Sometimes",
                "q_shared_groceries": "Agree",
                "q_work_from_home": "Often",
                "q_morning_routine": "Disagree",
                "q_social_events": "Sometimes",
                "q_tv_music": "Neutral",
                "q_visitors_notice": "Yes",
                "q_decorating": "Neutral",
                "q_conflict_style": "Agree",
                "q_budget_conscious": "Agree"
            }
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert "saved successfully" in data["message"].lower()

    def test_submit_survey_missing_username(self):
        """Test survey submission fails without username"""
        response = requests.post(f"{BASE_URL}/api/survey/submit", json={
            "answers": {"q_smoking": "No"}
        })
        assert response.status_code == 400
        data = response.json()
        assert "username" in data["message"].lower()

    def test_submit_survey_missing_answers(self):
        """Test survey submission fails without answers"""
        response = requests.post(f"{BASE_URL}/api/survey/submit", json={
            "username": "test@test.com"
        })
        assert response.status_code == 400
        data = response.json()
        assert "answers" in data["message"].lower()

    def test_submit_survey_empty_answers(self):
        """Test survey submission fails with empty answers"""
        response = requests.post(f"{BASE_URL}/api/survey/submit", json={
            "username": "test@test.com",
            "answers": {}
        })
        assert response.status_code == 400

    def test_submit_survey_updates_existing(self):
        """Test that submitting survey again updates existing answers"""
        unique_user = f"test_{uuid.uuid4().hex[:8]}@test.com"
        
        # Submit first time
        response1 = requests.post(f"{BASE_URL}/api/survey/submit", json={
            "username": unique_user,
            "answers": {"q_smoking": "Yes"}
        })
        assert response1.status_code == 200
        
        # Submit again with different answer
        response2 = requests.post(f"{BASE_URL}/api/survey/submit", json={
            "username": unique_user,
            "answers": {"q_smoking": "No"}
        })
        assert response2.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

