"""
Test Matches API Endpoint
Run with: python -m pytest test/backend/test_api_matches.py -v
"""
import requests
import pytest

BASE_URL = "http://localhost:5646"


class TestMatchesEndpoint:
    """Tests for the /api/matches/<user_id> endpoint"""

    def test_get_matches_for_valid_user(self):
        """Test getting matches for a user with completed survey"""
        response = requests.get(f"{BASE_URL}/api/matches/alice@wsu.edu")
        assert response.status_code == 200
        data = response.json()
        assert "matches" in data
        assert isinstance(data["matches"], list)

    def test_matches_have_required_fields(self):
        """Test that each match has required fields"""
        response = requests.get(f"{BASE_URL}/api/matches/alice@wsu.edu")
        data = response.json()
        
        required_fields = ["id", "name", "compatibility", "status"]
        for match in data["matches"]:
            for field in required_fields:
                assert field in match, f"Match missing required field: {field}"

    def test_matches_sorted_by_compatibility(self):
        """Test that matches are sorted by compatibility (highest first)"""
        response = requests.get(f"{BASE_URL}/api/matches/alice@wsu.edu")
        data = response.json()
        
        compatibilities = [m["compatibility"] for m in data["matches"]]
        assert compatibilities == sorted(compatibilities, reverse=True), \
            "Matches should be sorted by compatibility (highest first)"

    def test_compatibility_scores_in_range(self):
        """Test that compatibility scores are between 0 and 100"""
        response = requests.get(f"{BASE_URL}/api/matches/alice@wsu.edu")
        data = response.json()
        
        for match in data["matches"]:
            assert 0 <= match["compatibility"] <= 100, \
                f"Compatibility {match['compatibility']} out of range"

    def test_user_not_matched_with_self(self):
        """Test that user is not in their own matches"""
        response = requests.get(f"{BASE_URL}/api/matches/alice@wsu.edu")
        data = response.json()
        
        match_ids = [m["id"] for m in data["matches"]]
        assert "alice@wsu.edu" not in match_ids, "User should not match with themselves"

    def test_get_matches_for_user_without_survey(self):
        """Test getting matches for user who hasn't completed survey"""
        response = requests.get(f"{BASE_URL}/api/matches/nonexistent@test.com")
        assert response.status_code == 404
        data = response.json()
        assert "not completed" in data["message"].lower() or "matches" in data

    def test_matches_return_profile_info(self):
        """Test that matches include profile information"""
        response = requests.get(f"{BASE_URL}/api/matches/alice@wsu.edu")
        data = response.json()
        
        if len(data["matches"]) > 0:
            match = data["matches"][0]
            # These fields may be None but should exist
            assert "age" in match
            assert "major" in match
            assert "bio" in match


class TestMatchingAlgorithm:
    """Tests for the matching algorithm behavior"""

    def test_similar_users_have_high_compatibility(self):
        """Test that Alice and Carol (both quiet/clean) have high compatibility"""
        response = requests.get(f"{BASE_URL}/api/matches/alice@wsu.edu")
        data = response.json()
        
        carol_match = next((m for m in data["matches"] if m["id"] == "carol@wsu.edu"), None)
        assert carol_match is not None, "Carol should be in Alice's matches"
        assert carol_match["compatibility"] >= 70, \
            f"Alice and Carol should have high compatibility, got {carol_match['compatibility']}"

    def test_different_users_have_lower_compatibility(self):
        """Test that opposite lifestyle users have lower compatibility"""
        response = requests.get(f"{BASE_URL}/api/matches/alice@wsu.edu")
        data = response.json()
        
        # Bob is a night owl who likes loud music - opposite of Alice
        bob_match = next((m for m in data["matches"] if m["id"] == "bob@wsu.edu"), None)
        assert bob_match is not None, "Bob should be in Alice's matches"
        assert bob_match["compatibility"] < 70, \
            f"Alice and Bob should have lower compatibility, got {bob_match['compatibility']}"

    def test_matching_is_symmetric(self):
        """Test that if A matches with B at X%, B matches with A at X%"""
        response_alice = requests.get(f"{BASE_URL}/api/matches/alice@wsu.edu")
        response_carol = requests.get(f"{BASE_URL}/api/matches/carol@wsu.edu")
        
        alice_data = response_alice.json()
        carol_data = response_carol.json()
        
        # Find Carol in Alice's matches
        carol_in_alice = next((m for m in alice_data["matches"] if m["id"] == "carol@wsu.edu"), None)
        # Find Alice in Carol's matches
        alice_in_carol = next((m for m in carol_data["matches"] if m["id"] == "alice@wsu.edu"), None)
        
        assert carol_in_alice is not None
        assert alice_in_carol is not None
        assert carol_in_alice["compatibility"] == alice_in_carol["compatibility"], \
            "Matching should be symmetric"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

