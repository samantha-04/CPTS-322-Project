"""
Test Questions API Endpoint
Run with: python -m pytest test/backend/test_api_questions.py -v
"""
import requests
import pytest

BASE_URL = "http://localhost:5646"


class TestQuestionsEndpoint:
    """Tests for the /api/questions endpoint"""

    def test_get_questions_returns_200(self):
        """Test that questions endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/questions")
        assert response.status_code == 200

    def test_get_questions_returns_dict(self):
        """Test that questions endpoint returns a dictionary"""
        response = requests.get(f"{BASE_URL}/api/questions")
        data = response.json()
        assert isinstance(data, dict)

    def test_questions_have_required_fields(self):
        """Test that each question has type, label, and weight"""
        response = requests.get(f"{BASE_URL}/api/questions")
        data = response.json()
        
        for key, question in data.items():
            assert "label" in question, f"Question {key} missing 'label'"
            assert "weight" in question, f"Question {key} missing 'weight'"
            # type can be null for free-text questions

    def test_questions_have_valid_types(self):
        """Test that questions have valid types"""
        valid_types = ["yes_no", "likert_5", "frequency_4", None]
        response = requests.get(f"{BASE_URL}/api/questions")
        data = response.json()
        
        for key, question in data.items():
            assert question.get("type") in valid_types, f"Question {key} has invalid type"

    def test_questions_count(self):
        """Test that there are a reasonable number of questions"""
        response = requests.get(f"{BASE_URL}/api/questions")
        data = response.json()
        assert len(data) >= 10, "Should have at least 10 questions"
        assert len(data) <= 50, "Should not have more than 50 questions"

    def test_legacy_endpoint_also_works(self):
        """Test that /questions (legacy) also works"""
        response = requests.get(f"{BASE_URL}/questions")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

