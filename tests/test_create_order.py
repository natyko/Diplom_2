import allure


@allure.epic("Stellar Burgers API")
@allure.feature("Order Creation")
class TestCreateOrder:

    @allure.title("Create order with valid ingredients as authorized user")
    @allure.description(
        "Authorized user can create an order with valid ingredient IDs and receive an order number."
    )
    def test_create_order_with_auth(self, authenticated_user, ingredient_ids):
        with allure.step("Create order with valid ingredients"):
            order_resp = authenticated_user.create_order(ingredient_ids, with_auth=True)
            assert order_resp.status_code == 200, "Expected 200 when creating order with auth"
            body = order_resp.json()
            assert body.get("success") is True
            assert "order" in body and isinstance(
                body["order"].get("number"), int
            ), "No order number in response"

    @allure.title("Create order without authorization token")
    @allure.description(
        "Attempt to create an order without being authenticated should succeed (if allowed by system)."
    )
    def test_create_order_without_auth(self, api_client, ingredient_ids):
        with allure.step("Create order without authentication"):
            response = api_client.create_order(ingredient_ids, with_auth=False)
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
            body = response.json()
            assert body.get("success") is True
            assert "order" in body
            assert isinstance(body["order"].get("number"), int)

    @allure.title("Create order with no ingredients (negative)")
    @allure.description(
        "Creating an order without providing ingredient IDs should return 400 Bad Request."
    )
    def test_create_order_no_ingredients(self, authenticated_user):
        with allure.step("Create order with empty ingredients list"):
            response = authenticated_user.create_order([], with_auth=True)
            assert response.status_code == 400, "Expected 400 Bad Request when no ingredients provided"
            error = response.json()
            assert (
                error.get("message") == "Ingredient ids must be provided"
            ), f"Unexpected error message: {error.get('message')}"

    @allure.title("Create order with invalid ingredient ID (negative)")
    @allure.description(
        "Using an invalid ingredient hash for order creation should result in an internal server error."
    )
    def test_create_order_invalid_ingredient(self, authenticated_user):
        with allure.step("Create order with invalid ingredient ID"):
            invalid_id = "12345invalidID"
            response = authenticated_user.create_order([invalid_id], with_auth=True)
            assert response.status_code == 500, "Expected 500 Internal Server Error for invalid ingredient ID"
