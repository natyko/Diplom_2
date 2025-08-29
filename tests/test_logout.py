import allure
from utils.user_data import generate_unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("User Logout")
class TestLogout:

    @allure.title("Logout with refresh token")
    @allure.description(
        "Successfully logout using refresh token obtained during registration."
    )
    def test_logout_with_refresh_token(self, api_client):
        with allure.step("Register user and logout with refresh token"):
            user = generate_unique_user()
            reg_resp = api_client.register_user(user)
            assert reg_resp.status_code == 200
            refresh_token = reg_resp.json().get("refreshToken")
            assert refresh_token, "Refresh token not returned"
            
            logout_resp = api_client.logout_user(refresh_token)
            assert logout_resp.status_code == 200
            assert logout_resp.json()["success"] is True
            assert logout_resp.json()["message"] == "Successful logout"
