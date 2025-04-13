import allure
import requests

from utils.api_urls import ORDERS_URL, INGREDIENTS_URL, REGISTER_URL
from utils.user_data import generate_unique_user


@allure.epic("Stellar Burgers API")
@allure.feature("Order Creation")
class TestCreateOrder:

    @allure.title("Create order with valid ingredients as authorized user")
    @allure.description(
        "Authorized user can create an order with valid ingredient IDs and receive an order number."
    )
    def test_create_order_with_auth(self):
        # Register & login to get token
        user = generate_unique_user()
        auth_token = requests.post(REGISTER_URL, json=user).json()["accessToken"]
        headers = {"Authorization": auth_token}
        # Get available ingredient IDs from the ingredients API
        ingredients_resp = requests.get(INGREDIENTS_URL)
        assert ingredients_resp.status_code == 200, "Failed to fetch ingredients"
        ingredients_data = ingredients_resp.json()
        assert ingredients_data.get("success") is True
        # Pick at least two ingredient IDs for the order
        ingredient_ids = [item["_id"] for item in ingredients_data["data"]][:2]
        with allure.step("Send POST /orders with valid ingredients and auth token"):
            order_resp = requests.post(
                ORDERS_URL, headers=headers, json={"ingredients": ingredient_ids}
            )
            assert (
                order_resp.status_code == 200
            ), "Expected 200 when creating order with auth"
        with allure.step("Verify order creation response contains order number"):
            body = order_resp.json()
            assert body.get("success") is True
            assert "order" in body and isinstance(
                body["order"].get("number"), int
            ), "No order number in response"

    @allure.title("Create order without authorization token")
    @allure.description(
        "Attempt to create an order without being authenticated should succeed (if allowed by system)."
    )
    def test_create_order_without_auth(self):
        # Get ingredients
        ingredients = requests.get(INGREDIENTS_URL).json()["data"]
        ingredient_ids = [item["_id"] for item in ingredients][:2]

        with allure.step("Send POST /orders without auth token"):
            response = requests.post(ORDERS_URL, json={"ingredients": ingredient_ids})

        with allure.step("Verify order creation succeeds for unauthenticated user"):
            assert (
                response.status_code == 200
            ), f"Unexpected status code: {response.status_code}"
            body = response.json()
            assert body.get("success") is True
            assert "order" in body
            assert isinstance(body["order"].get("number"), int)

    @allure.title("Create order with no ingredients (negative)")
    @allure.description(
        "Creating an order without providing ingredient IDs should return 400 Bad Request."
    )
    def test_create_order_no_ingredients(self):
        # Create a user and get token for auth
        user = generate_unique_user()
        token = requests.post(REGISTER_URL, json=user).json()["accessToken"]
        headers = {"Authorization": token}
        with allure.step("Send POST /orders with empty ingredients list"):
            response = requests.post(
                ORDERS_URL, headers=headers, json={"ingredients": []}
            )
            assert (
                response.status_code == 400
            ), "Expected 400 Bad Request when no ingredients provided"
        with allure.step("Verify error message for missing ingredients"):
            error = response.json()
            assert (
                error.get("message") == "Ingredient ids must be provided"
            ), f"Unexpected error message: {error.get('message')}"

    @allure.title("Create order with invalid ingredient ID (negative)")
    @allure.description(
        "Using an invalid ingredient hash for order creation should result in an internal server error."
    )
    def test_create_order_invalid_ingredient(self):
        # Create authorized user
        user = generate_unique_user()
        token = requests.post(REGISTER_URL, json=user).json()["accessToken"]
        headers = {"Authorization": token}
        invalid_id = "12345invalidID"
        with allure.step("Send POST /orders with an invalid ingredient ID"):
            response = requests.post(
                ORDERS_URL, headers=headers, json={"ingredients": [invalid_id]}
            )
            assert (
                response.status_code == 500
            ), "Expected 500 Internal Server Error for invalid ingredient ID"
