"""
Pytest Configuration
"""
import pytest
import requests

BASE_URL = "http://localhost:5646"
FRONTEND_URL = "http://localhost:8000"


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


@pytest.fixture(scope="session", autouse=True)
def check_services_running():
    """Check that backend and frontend are running before tests"""
    try:
        backend_response = requests.get(f"{BASE_URL}/health", timeout=5)
        assert backend_response.status_code == 200, "Backend not responding correctly"
    except requests.exceptions.ConnectionError:
        pytest.exit("Backend is not running! Start it with 'docker-compose up -d' or 'make start'")
    
    try:
        frontend_response = requests.get(FRONTEND_URL, timeout=5)
        assert frontend_response.status_code == 200, "Frontend not responding correctly"
    except requests.exceptions.ConnectionError:
        pytest.exit("Frontend is not running! Start it with 'docker-compose up -d' or 'make start'")


@pytest.fixture
def api_base_url():
    """Fixture providing the API base URL"""
    return BASE_URL


@pytest.fixture
def frontend_base_url():
    """Fixture providing the frontend base URL"""
    return FRONTEND_URL

