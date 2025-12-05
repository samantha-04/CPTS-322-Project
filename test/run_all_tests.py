#!/usr/bin/env python3
"""
Run All Tests
Usage: python test/run_all_tests.py

This script runs all tests and provides a summary report.
Make sure the backend (localhost:5646) and frontend (localhost:8000) are running first!
"""
import subprocess
import sys
import os

# Change to project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)

def run_tests():
    print("=" * 60)
    print("ROOMMATE FINDER - TEST SUITE")
    print("=" * 60)
    print()
    print("Prerequisites:")
    print("  - Backend running on http://localhost:5646")
    print("  - Frontend running on http://localhost:8000")
    print()
    print("Starting tests...")
    print("-" * 60)
    
    # Run pytest with verbose output
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "test/", "-v", "--tb=short"],
        cwd=project_root
    )
    
    print()
    print("=" * 60)
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
        print("   Check the output above for details.")
    print("=" * 60)
    
    return result.returncode


def run_quick_tests():
    """Run only fast tests (skip integration)"""
    print("Running quick tests (unit tests only)...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "test/backend/test_matching_algorithm.py", "-v"],
        cwd=project_root
    )
    return result.returncode


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        sys.exit(run_quick_tests())
    else:
        sys.exit(run_tests())

