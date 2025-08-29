import pytest
import allure
from utils.api_client import StellarBurgersAPI
from utils.user_data import generate_unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("User Registration")
class TestUserRegistration:

    @allure.title("Create a new unique user (positive)")
    @allure.description(
        "Register a new user with unique email, expecting a successful response with access token."
    )
    def test_create_unique_user(self, api_client):
        with allure.step("Register new user and verify successful response"):
            new_user = generate_unique_user()
            response = api_client.register_user(new_user)
            assert response.status_code == 200, "Expected 200 OK for successful registration"
            body = response.json()
            assert body.get("success") is True, "Response 'success' should be True"
            assert "accessToken" in body and body["accessToken"].startswith(
                "Bearer "
            ), "No accessToken in response"
            assert "refreshToken" in body, "No refreshToken in response"
            assert body["user"]["email"] == new_user["email"]
            assert body["user"]["name"] == new_user["name"]

    @allure.title("Create an already registered user (negative)")
    @allure.description(
        "Attempt to register a user that already exists, expecting a 403 error."
    )
    def test_create_existing_user(self, api_client):
        with allure.step("Register user first time"):
            user = generate_unique_user()
            first_response = api_client.register_user(user)
            assert first_response.status_code == 200, "First registration should succeed"
        
        with allure.step("Attempt duplicate registration and verify error"):
            # Create new API client to avoid auth token conflicts
            second_api = StellarBurgersAPI()
            response = second_api.register_user(user)
            assert response.status_code == 403, "Expected 403 Forbidden for duplicate registration"
            error = response.json()
            assert (
                error.get("message") == "User already exists"
            ), f"Unexpected error message: {error.get('message')}"

    @allure.title("Create user with missing required field (negative)")
    @allure.description(
        "Attempt to register with a missing field (email, password, or name) should fail with 403."
    )
    @pytest.mark.parametrize("field_to_omit", ["email", "password", "name"])
    def test_create_user_missing_field(self, api_client, field_to_omit):
        with allure.step(f"Register user without '{field_to_omit}' field and verify error"):
            base_data = generate_unique_user()
            user_data = {k: v for k, v in base_data.items() if k != field_to_omit}
            response = api_client.register_user(user_data)
            assert response.status_code == 403, "Expected 403 when a required field is missing"
            error = response.json()
            assert (
                error.get("message") == "Email, password and name are required fields"
            ), f"Unexpected error message: {error.get('message')}"
