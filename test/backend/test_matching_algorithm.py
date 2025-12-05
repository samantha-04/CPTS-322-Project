"""
Test Matching Algorithm (Unit Tests)
Run with: python -m pytest test/backend/test_matching_algorithm.py -v

NOTE: Requires numpy to be installed. Skip if running outside of virtual environment.
"""
import pytest
import sys
from pathlib import Path

# Try to import the matching module - skip tests if dependencies not available
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "code" / "backend"))
    from Matching.Matching import Match
    MATCHING_AVAILABLE = True
except ImportError:
    MATCHING_AVAILABLE = False
    Match = None


@pytest.mark.skipif(not MATCHING_AVAILABLE, reason="numpy or Matching module not available")
class TestMatchFunction:
    """Unit tests for the Match function"""

    def test_identical_vectors_perfect_match(self):
        """Test that identical vectors return ~1.0 (perfect match)"""
        user1 = [1.0, 0.5, -0.5, 0.0, 1.0]
        user2 = [1.0, 0.5, -0.5, 0.0, 1.0]
        
        result = Match(user1, user2)
        assert abs(result - 1.0) < 0.001, f"Identical vectors should match perfectly, got {result}"

    def test_opposite_vectors_no_match(self):
        """Test that opposite vectors return ~-1.0 (no match)"""
        user1 = [1.0, 1.0, 1.0, 1.0, 1.0]
        user2 = [-1.0, -1.0, -1.0, -1.0, -1.0]
        
        result = Match(user1, user2)
        assert abs(result - (-1.0)) < 0.001, f"Opposite vectors should not match, got {result}"

    def test_orthogonal_vectors_neutral(self):
        """Test that orthogonal vectors return ~0 (neutral)"""
        user1 = [1.0, 0.0, 0.0, 0.0]
        user2 = [0.0, 1.0, 0.0, 0.0]
        
        result = Match(user1, user2)
        assert abs(result) < 0.001, f"Orthogonal vectors should be neutral, got {result}"

    def test_match_returns_float(self):
        """Test that Match returns a float"""
        user1 = [1.0, 0.5, -0.5]
        user2 = [0.5, 0.5, 0.0]
        
        result = Match(user1, user2)
        assert isinstance(result, float)

    def test_match_is_symmetric(self):
        """Test that Match(A, B) == Match(B, A)"""
        user1 = [1.0, 0.5, -0.5, 0.3, 0.8]
        user2 = [0.2, -0.3, 0.7, 0.1, -0.5]
        
        result1 = Match(user1, user2)
        result2 = Match(user2, user1)
        
        assert abs(result1 - result2) < 0.001, "Matching should be symmetric"

    def test_match_in_valid_range(self):
        """Test that Match always returns value between -1 and 1"""
        test_cases = [
            ([1.0, 1.0, 1.0], [1.0, 1.0, 1.0]),
            ([1.0, 1.0, 1.0], [-1.0, -1.0, -1.0]),
            ([0.5, -0.5, 0.0], [0.0, 0.5, -0.5]),
            ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0]),
        ]
        
        for user1, user2 in test_cases:
            result = Match(user1, user2)
            assert -1.0 <= result <= 1.0, f"Match result {result} out of range for {user1}, {user2}"

    def test_similar_preferences_high_score(self):
        """Test that similar (but not identical) preferences have high score"""
        # Both prefer quiet, clean, early schedule
        user1 = [1.0, 0.8, 0.9, -0.5, -0.7]
        user2 = [0.9, 0.7, 0.8, -0.6, -0.8]
        
        result = Match(user1, user2)
        assert result > 0.9, f"Similar preferences should have high score, got {result}"

    def test_mixed_preferences_medium_score(self):
        """Test that mixed preferences have medium score"""
        # Some agreement, some disagreement
        user1 = [1.0, 0.5, -0.5, 0.0, 1.0]
        user2 = [1.0, -0.5, 0.5, 0.0, 1.0]
        
        result = Match(user1, user2)
        assert 0.0 < result < 0.9, f"Mixed preferences should have medium score, got {result}"


@pytest.mark.skipif(not MATCHING_AVAILABLE, reason="numpy or Matching module not available")
class TestMatchEdgeCases:
    """Edge case tests for the Match function"""

    def test_single_dimension(self):
        """Test matching with single dimension vectors"""
        user1 = [1.0]
        user2 = [1.0]
        
        result = Match(user1, user2)
        assert abs(result - 1.0) < 0.001

    def test_large_vectors(self):
        """Test matching with larger vectors (20+ dimensions)"""
        import random
        user1 = [random.uniform(-1, 1) for _ in range(25)]
        user2 = [random.uniform(-1, 1) for _ in range(25)]
        
        result = Match(user1, user2)
        assert -1.0 <= result <= 1.0

    def test_all_zeros_handled(self):
        """Test that all-zero vectors are handled (should return some value)"""
        user1 = [0.0, 0.0, 0.0]
        user2 = [1.0, 0.0, 0.0]
        
        # This might raise an error or return a special value
        # depending on implementation
        try:
            result = Match(user1, user2)
            # If it returns, it should be a valid number
            assert isinstance(result, (int, float))
        except (ValueError, ZeroDivisionError):
            # Acceptable to raise error for zero vector
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
