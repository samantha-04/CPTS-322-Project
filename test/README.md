# Test Suite

This directory contains all tests for the Roommate Finder application.

## Prerequisites

Before running tests, make sure:

1. **Backend is running** on `http://localhost:5646`
2. **Frontend is running** on `http://localhost:8000`

Start both with:
```bash
make start
# or
docker-compose up -d
```

## Running Tests

### Run All Tests
```bash
python3 -m pytest test/ -v
```

### Run Specific Test Files
```bash
# API Health tests
python3 -m pytest test/backend/test_api_health.py -v

# Authentication tests
python3 -m pytest test/backend/test_api_auth.py -v

# Matches tests
python3 -m pytest test/backend/test_api_matches.py -v

# Survey tests
python3 -m pytest test/backend/test_api_survey.py -v

# Questions tests
python3 -m pytest test/backend/test_api_questions.py -v

# User profile tests
python3 -m pytest test/backend/test_api_user.py -v

# Matching algorithm unit tests (requires numpy)
python3 -m pytest test/backend/test_matching_algorithm.py -v

# Integration tests
python3 -m pytest test/integration/test_full_flow.py -v
```

### Using the Test Runner Script
```bash
python3 test/run_all_tests.py
```

## Test Structure

```
test/
├── README.md                 # This file
├── conftest.py              # Pytest configuration
├── run_all_tests.py         # Test runner script
├── backend/
│   ├── test_api_health.py   # Health endpoint tests
│   ├── test_api_auth.py     # Registration & login tests
│   ├── test_api_questions.py # Questions endpoint tests
│   ├── test_api_matches.py  # Matches endpoint & algorithm tests
│   ├── test_api_survey.py   # Survey submission tests
│   ├── test_api_user.py     # User profile tests
│   └── test_matching_algorithm.py  # Unit tests for matching
└── integration/
    └── test_full_flow.py    # End-to-end integration tests
```

## Test Coverage

| Test File | Tests | Description |
|-----------|-------|-------------|
| `test_api_health.py` | 3 | Health check endpoint |
| `test_api_auth.py` | 10 | Registration & login |
| `test_api_questions.py` | 6 | Questions endpoint |
| `test_api_matches.py` | 10 | Matches & algorithm |
| `test_api_survey.py` | 5 | Survey submission |
| `test_api_user.py` | 8 | User profiles |
| `test_matching_algorithm.py` | 11 | Unit tests (requires numpy) |
| `test_full_flow.py` | 8 | Integration tests |

## Demo Accounts for Testing

| Email | Password | Description |
|-------|----------|-------------|
| alice@wsu.edu | 123 | Quiet, clean, early riser |
| bob@wsu.edu | 123 | Night owl, social, music lover |
| carol@wsu.edu | 123 | Pre-med, very organized |
| david@wsu.edu | 123 | Flexible schedule, chill |
| emma@wsu.edu | 123 | Outgoing, pet lover |

## Expected Output

```
==================== test session starts ====================
collected 61 items

test/backend/test_api_auth.py::TestRegistrationEndpoint::test_register_new_user PASSED
test/backend/test_api_auth.py::TestLoginEndpoint::test_login_valid_credentials PASSED
...
test/integration/test_full_flow.py::TestFullUserFlow::test_complete_registration_to_matches_flow PASSED

==================== 50 passed, 11 skipped in 1.13s ====================
```

Note: 11 tests may be skipped if numpy is not installed locally (matching algorithm unit tests).

