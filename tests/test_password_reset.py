import requests
import allure

from utils.user_data import generate_unique_user
from utils.api_urls import PASSWORD_RESET_CONFIRM_URL


@allure.epic("Stellar Burgers API")
@allure.feature("Password Reset")
class TestPasswordReset:

    @allure.title("Password reset request")
    @allure.description("Request password reset email for a registered user.")
    def test_request_password_reset_email(self, api_client):
        with allure.step("Request password reset and verify response"):
            email = f"reset_test_{generate_unique_user()['email']}"
            response = api_client.request_password_reset(email)
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert response.json()["message"] == "Reset email sent"

    @allure.title("Password reset final step with fake token")
    @allure.description("Attempt to reset password using an invalid token.")
    def test_password_reset_with_invalid_token(self, api_client):
        with allure.step("Attempt password reset with invalid token and verify error"):
            response = requests.post(
                PASSWORD_RESET_CONFIRM_URL,
                json={"password": "newpass123", "token": "invalid-token-123"},
            )
            assert response.status_code in [403, 404, 500]
            assert response.json()["success"] is False
