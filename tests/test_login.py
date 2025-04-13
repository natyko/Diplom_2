import allure
import requests

from utils.api_urls import LOGIN_URL, REGISTER_URL
from utils.user_data import generate_unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("User Login")
class TestUserLogin:

    @allure.title("Login with existing user credentials (positive)")
    @allure.description(
        "Login with correct email and password should succeed and return an access token."
    )
    def test_login_success(self):
        # Ensure a user exists by registering first
        user = generate_unique_user()
        requests.post(REGISTER_URL, json=user)
        with allure.step("Send POST /auth/login with valid credentials"):
            response = requests.post(
                LOGIN_URL, json={"email": user["email"], "password": user["password"]}
            )
            assert response.status_code == 200, "Expected 200 OK for successful login"
        with allure.step("Verify response contains tokens and user info"):
            body = response.json()
            assert body.get("success") is True
            assert "accessToken" in body and body["accessToken"].startswith("Bearer ")
            assert "refreshToken" in body
            assert body["user"]["email"] == user["email"]
            assert body["user"]["name"] == user["name"]

    @allure.title("Login with incorrect password (negative)")
    @allure.description(
        "Attempt to login with an incorrect password should return 401 Unauthorized."
    )
    def test_login_incorrect_password(self):
        # Create a user first
        user = generate_unique_user()
        requests.post(REGISTER_URL, json=user)
        wrong_credentials = {"email": user["email"], "password": "WrongPassword123"}
        with allure.step("Send POST /auth/login with incorrect password"):
            response = requests.post(LOGIN_URL, json=wrong_credentials)
            # Wrong email or password 401 Unauthorized
            assert (
                response.status_code == 401
            ), "Expected 401 Unauthorized for invalid login"
        with allure.step("Verify error message for incorrect credentials"):
            error = response.json()
            assert (
                error.get("message") == "email or password are incorrect"
            ), f"Unexpected error message: {error.get('message')}"
