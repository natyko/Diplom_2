import allure
import requests

from utils.api_urls import USER_URL, REGISTER_URL
from utils.user_data import generate_unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("User Profile Update")
class TestUserUpdate:

    @allure.title("Update user name and email with authorization (positive)")
    @allure.description(
        "Authenticated user can update their name and email successfully."
    )
    def test_update_user_with_auth(self):
        # Register and login to get a token
        user = generate_unique_user()
        reg_resp = requests.post(REGISTER_URL, json=user).json()
        token = reg_resp["accessToken"]
        # Update user profile
        new_name = "NewName"
        new_email = f"new_{user['email']}"
        headers = {"Authorization": token}
        with allure.step("Send PATCH /auth/user with valid token and new name & email"):
            update_resp = requests.patch(
                USER_URL, headers=headers, json={"name": new_name, "email": new_email}
            )
            assert (
                update_resp.status_code == 200
            ), "Expected 200 OK for valid profile update"
        with allure.step("Verify response contains updated user data"):
            body = update_resp.json()
            assert body.get("success") is True
            assert body["user"]["name"] == new_name
            assert body["user"]["email"] == new_email

    @allure.title("Update user data without authorization (negative)")
    @allure.description(
        "Attempt to update user profile without a token should fail with 401 and no data change."
    )
    def test_update_user_without_auth(self):
        # Create a user and get their token and current data
        user = generate_unique_user()
        reg = requests.post(REGISTER_URL, json=user).json()
        token = reg["accessToken"]
        original_name = user["name"]
        # Attempt to update without providing auth header
        new_name = "UnauthorizedName"
        with allure.step("Send PATCH /auth/user without token in header"):
            response = requests.patch(USER_URL, json={"name": new_name})
            assert response.status_code == 401, "Expected 401 for update without auth"
        with allure.step("Verify error message and no change in user data"):
            error = response.json()
            assert (
                error.get("message") == "You should be authorised"
            ), f"Unexpected error message: {error.get('message')}"
            headers = {"Authorization": token}
            profile_resp = requests.get(USER_URL, headers=headers)
            assert profile_resp.status_code == 200
            profile = profile_resp.json()
            assert (
                profile["user"]["name"] == original_name
            ), "User name changed despite unauthorized update!"
