import allure


@allure.epic("Stellar Burgers API")
@allure.feature("User Profile Update")
class TestUserUpdate:

    @allure.title("Update user name and email with authorization (positive)")
    @allure.description(
        "Authenticated user can update their name and email successfully."
    )
    def test_update_user_with_auth(self, authenticated_user):
        with allure.step("Update user profile and verify changes"):
            new_name = "NewName"
            # Get current user email to modify it
            user_info_resp = authenticated_user.get_user_info()
            assert user_info_resp.status_code == 200, "Failed to get user info"
            current_email = user_info_resp.json()["user"]["email"]
            new_email = f"new_{current_email}"
            
            update_resp = authenticated_user.update_user({"name": new_name, "email": new_email})
            assert update_resp.status_code == 200, "Expected 200 OK for valid profile update"
            body = update_resp.json()
            assert body.get("success") is True
            assert body["user"]["name"] == new_name
            assert body["user"]["email"] == new_email

    @allure.title("Update user data without authorization (negative)")
    @allure.description(
        "Attempt to update user profile without a token should fail with 401 and no data change."
    )
    def test_update_user_without_auth(self, authenticated_user):
        with allure.step("Attempt unauthorized update and verify error"):
            # Get original user data for verification
            user_info_resp = authenticated_user.get_user_info()
            assert user_info_resp.status_code == 200, "Failed to get user info"
            original_name = user_info_resp.json()["user"]["name"]
            
            # Make unauthorized request using raw requests
            import requests
            from utils.api_urls import USER_URL
            new_name = "UnauthorizedName"
            response = requests.patch(USER_URL, json={"name": new_name})
            assert response.status_code == 401, "Expected 401 for update without auth"
            error = response.json()
            assert (
                error.get("message") == "You should be authorised"
            ), f"Unexpected error message: {error.get('message')}"
            
            # Verify user data unchanged
            profile_resp = authenticated_user.get_user_info()
            assert profile_resp.status_code == 200
            profile = profile_resp.json()
            assert (
                profile["user"]["name"] == original_name
            ), "User name changed despite unauthorized update!"
