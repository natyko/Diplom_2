import pytest
import requests
import allure
from utils.api_urls import BASE_URL, REGISTER_URL
from utils.user_data import generate_unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("User Registration")
class TestUserRegistration:

    @allure.title("Create a new unique user (positive)")
    @allure.description(
        "Register a new user with unique email, expecting a successful response with access token."
    )
    def test_create_unique_user(self):
        # Generate unique user data
        new_user = generate_unique_user()
        with allure.step("Send POST /auth/register with valid unique user data"):
            response = requests.post(REGISTER_URL, json=new_user)
            assert (
                response.status_code == 200
            ), "Expected 200 OK for successful registration"
        with allure.step("Verify response contains success status and tokens"):
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
    def test_create_existing_user(self):
        # Prepare a user and register once
        user = generate_unique_user()
        requests.post(REGISTER_URL, json=user)
        with allure.step("Re-send POST /auth/register with the same user data"):
            response = requests.post(REGISTER_URL, json=user)
            assert (
                response.status_code == 403
            ), "Expected 403 Forbidden for duplicate registration"
        with allure.step("Verify error message for existing user"):
            error = response.json()
            assert (
                error.get("message") == "User already exists"
            ), f"Unexpected error message: {error.get('message')}"

    @allure.title("Create user with missing required field (negative)")
    @allure.description(
        "Attempt to register with a missing field (email, password, or name) should fail with 403."
    )
    @pytest.mark.parametrize("field_to_omit", ["email", "password", "name"])
    def test_create_user_missing_field(self, field_to_omit):
        base_data = generate_unique_user()
        # Remove one required field
        user_data = {k: v for k, v in base_data.items() if k != field_to_omit}
        with allure.step(
            f"Send POST /auth/register without the '{field_to_omit}' field"
        ):
            response = requests.post(REGISTER_URL, json=user_data)
            assert (
                response.status_code == 403
            ), "Expected 403 when a required field is missing"
        with allure.step("Verify error message for missing field"):
            error = response.json()
            assert (
                error.get("message") == "Email, password and name are required fields"
            ), f"Unexpected error message: {error.get('message')}"
