import allure

from utils.api_client import StellarBurgersAPI
from utils.user_data import generate_unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("User Login")
class TestUserLogin:

    @allure.title("Login with existing user credentials (positive)")
    @allure.description(
        "Login with correct email and password should succeed and return an access token."
    )
    def test_login_success(self, api_client):
        with allure.step("Register user for login test"):
            user = generate_unique_user()
            reg_response = api_client.register_user(user)
            assert reg_response.status_code == 200, "Registration should succeed"
        
        with allure.step("Login with valid credentials and verify response"):
            # Create new API client for clean login test
            login_api = StellarBurgersAPI()
            response = login_api.login_user(user["email"], user["password"])
            assert response.status_code == 200, "Expected 200 OK for successful login"
            body = response.json()
            assert body.get("success") is True
            assert "accessToken" in body and body["accessToken"].startswith("Bearer ")
            assert "refreshToken" in body
            assert body["user"]["email"] == user["email"]
            assert body["user"]["name"] == user["name"]
            # Clean up the login API client
            login_api.created_users.append(user)
            login_api.cleanup_users()

    @allure.title("Login with incorrect password (negative)")
    @allure.description(
        "Attempt to login with an incorrect password should return 401 Unauthorized."
    )
    def test_login_incorrect_password(self, api_client):
        with allure.step("Register user and attempt login with wrong password"):
            user = generate_unique_user()
            reg_response = api_client.register_user(user)
            assert reg_response.status_code == 200, "Registration should succeed"
            
            # Create new API client for clean login test
            login_api = StellarBurgersAPI()
            response = login_api.login_user(user["email"], "WrongPassword123")
            assert response.status_code == 401, "Expected 401 Unauthorized for invalid login"
            error = response.json()
            assert (
                error.get("message") == "email or password are incorrect"
            ), f"Unexpected error message: {error.get('message')}"
