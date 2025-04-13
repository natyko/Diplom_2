import allure
import requests

from utils.api_urls import REGISTER_URL, INGREDIENTS_URL, ORDERS_URL
from utils.user_data import generate_unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("User Order History")
class TestUserOrders:

    @allure.title("Retrieve orders for an authenticated user (positive)")
    @allure.description(
        "Authenticated user should be able to fetch their order history."
    )
    def test_get_user_orders_with_auth(self):
        # Create user, login and create an order
        user = generate_unique_user()
        login_data = requests.post(REGISTER_URL, json=user).json()
        token = login_data["accessToken"]
        headers = {"Authorization": token}
        # Create an order to ensure there's at least one order in history
        ingredient_ids = [requests.get(INGREDIENTS_URL).json()["data"][0]["_id"]]
        requests.post(ORDERS_URL, headers=headers, json={"ingredients": ingredient_ids})
        with allure.step("Send GET /orders with valid auth token"):
            response = requests.get(ORDERS_URL, headers=headers)
            assert (
                response.status_code == 200
            ), "Expected 200 OK for fetching user orders"
        with allure.step("Verify response contains orders list"):
            data = response.json()
            assert data.get("success") is True
            assert "orders" in data, "Response should contain 'orders'"
            if data["orders"]:
                assert isinstance(
                    data["orders"][0].get("number"), int
                ), "Order entry missing 'number' field"

    @allure.title("Retrieve user orders without auth (negative)")
    @allure.description(
        "Requesting order history without a token should be unauthorized."
    )
    def test_get_user_orders_without_auth(self):
        with allure.step("Send GET /orders without auth header"):
            response = requests.get(ORDERS_URL)  # no headers
            assert (
                response.status_code == 401
            ), "Expected 401 for fetching orders without auth"
        with allure.step("Verify error message for unauthorized request"):
            error = response.json()
            assert (
                error.get("message") == "You should be authorised"
            ), f"Unexpected error message: {error.get('message')}"
