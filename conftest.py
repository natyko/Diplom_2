import pytest
from utils.api_client import StellarBurgersAPI


@pytest.fixture(scope="function")
def api_client():
    """Provide a fresh API client for each test with automatic cleanup"""
    client = StellarBurgersAPI()
    yield client
    # Cleanup after test
    client.cleanup_users()


@pytest.fixture(scope="function")
def authenticated_user(api_client):
    """Provide an authenticated user for tests that need one"""
    register_resp = api_client.register_user()
    if register_resp.status_code != 200:
        pytest.fail(f"Failed to create test user: {register_resp.status_code}")
    return api_client


@pytest.fixture(scope="function")
def ingredient_ids(api_client):
    """Provide a list of valid ingredient IDs for testing"""
    ingredients_resp = api_client.get_ingredients()
    if ingredients_resp.status_code != 200:
        pytest.fail("Failed to fetch ingredients for test setup")
    
    ingredients_data = ingredients_resp.json()
    if not ingredients_data.get("success"):
        pytest.fail("Ingredients API returned success=false")
    
    return [item["_id"] for item in ingredients_data["data"]][:2]