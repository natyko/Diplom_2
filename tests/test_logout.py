import requests
import allure
from utils.api_urls import REGISTER_URL, LOGOUT_URL
from utils.user_data import generate_unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("User Logout")
class TestLogout:

    @allure.title("Logout with refresh token")
    @allure.description(
        "Successfully logout using refresh token obtained during registration."
    )
    def test_logout_with_refresh_token(self):
        user = generate_unique_user()

        with allure.step("Register new user and get refresh token"):
            reg_resp = requests.post(REGISTER_URL, json=user)
            assert reg_resp.status_code == 200
            refresh_token = reg_resp.json().get("refreshToken")
            assert refresh_token, "Refresh token not returned"

        with allure.step("Send POST /auth/logout with refresh token"):
            logout_resp = requests.post(LOGOUT_URL, json={"token": refresh_token})
            assert logout_resp.status_code == 200
            assert logout_resp.json()["success"] is True
            assert logout_resp.json()["message"] == "Successful logout"
