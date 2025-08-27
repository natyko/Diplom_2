import allure


@allure.epic("Stellar Burgers API")
@allure.feature("User Order History")
class TestUserOrders:

    @allure.title("Retrieve orders for an authenticated user (positive)")
    @allure.description(
        "Authenticated user should be able to fetch their order history."
    )
    def test_get_user_orders_with_auth(self, authenticated_user, ingredient_ids):
        with allure.step("Create an order to ensure order history exists"):
            order_resp = authenticated_user.create_order(ingredient_ids[:1], with_auth=True)
            assert order_resp.status_code == 200, "Failed to create test order"
        
        with allure.step("Fetch user orders and verify response"):
            response = authenticated_user.get_user_orders()
            assert response.status_code == 200, "Expected 200 OK for fetching user orders"
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
    def test_get_user_orders_without_auth(self, api_client):
        with allure.step("Fetch orders without authentication and verify error"):
            # Manually call the orders endpoint without auth
            import requests
            from utils.api_urls import ORDERS_URL
            response = requests.get(ORDERS_URL)  # no headers
            assert response.status_code == 401, "Expected 401 for fetching orders without auth"
            error = response.json()
            assert (
                error.get("message") == "You should be authorised"
            ), f"Unexpected error message: {error.get('message')}"
