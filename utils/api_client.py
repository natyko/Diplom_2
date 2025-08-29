import requests
from utils.api_urls import (
    REGISTER_URL, LOGIN_URL, LOGOUT_URL, USER_URL,
    ORDERS_URL, INGREDIENTS_URL, PASSWORD_RESET_URL
)
from utils.user_data import generate_unique_user


class StellarBurgersAPI:
    """API client for Stellar Burgers application"""
    
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.created_users = []  # Track users for cleanup
    
    def register_user(self, user_data=None):
        """Register a new user and return response"""
        if user_data is None:
            user_data = generate_unique_user()
        
        response = self.session.post(REGISTER_URL, json=user_data)
        if response.status_code == 200:
            self.created_users.append(user_data)
            self.auth_token = response.json().get("accessToken")
        return response
    
    def login_user(self, email, password):
        """Login user and return response"""
        user_data = {"email": email, "password": password}
        response = self.session.post(LOGIN_URL, json=user_data)
        if response.status_code == 200:
            self.auth_token = response.json().get("accessToken")
        return response
    
    def logout_user(self, refresh_token):
        """Logout user"""
        return self.session.post(LOGOUT_URL, json={"token": refresh_token})
    
    def get_user_info(self):
        """Get current user information"""
        headers = self._get_auth_headers()
        return self.session.get(USER_URL, headers=headers)
    
    def update_user(self, user_data):
        """Update user information"""
        headers = self._get_auth_headers()
        return self.session.patch(USER_URL, headers=headers, json=user_data)
    
    def get_ingredients(self):
        """Get available ingredients"""
        return self.session.get(INGREDIENTS_URL)
    
    def create_order(self, ingredients, with_auth=True):
        """Create an order with given ingredients"""
        headers = self._get_auth_headers() if with_auth else None
        order_data = {"ingredients": ingredients}
        return self.session.post(ORDERS_URL, headers=headers, json=order_data)
    
    def get_user_orders(self):
        """Get orders for authenticated user"""
        headers = self._get_auth_headers()
        return self.session.get(ORDERS_URL, headers=headers)
    
    def request_password_reset(self, email):
        """Request password reset"""
        return self.session.post(PASSWORD_RESET_URL, json={"email": email})
    
    def _get_auth_headers(self):
        """Get authorization headers"""
        if not self.auth_token:
            raise ValueError("No auth token available. Please login first.")
        return {"Authorization": self.auth_token}
    
    def delete_user(self):
        """Delete current authenticated user"""
        headers = self._get_auth_headers()
        return self.session.delete(USER_URL, headers=headers)
    
    def cleanup_users(self):
        """Clean up created users by attempting to delete them"""
        cleanup_errors = []
        
        # Try to delete each created user
        for user_data in self.created_users:
            try:
                # Login as the user first
                login_resp = self.login_user(user_data["email"], user_data["password"])
                if login_resp.status_code == 200:
                    # Try to delete the user
                    delete_resp = self.delete_user()
                    if delete_resp.status_code not in [200, 204, 404]:
                        cleanup_errors.append(f"Failed to delete user {user_data['email']}: {delete_resp.status_code}")
                else:
                    cleanup_errors.append(f"Failed to login user {user_data['email']} for cleanup")
            except Exception as e:
                cleanup_errors.append(f"Exception during cleanup for {user_data['email']}: {str(e)}")
        
        # Clear tracking regardless of success/failure
        self.created_users.clear()
        self.auth_token = None
        
        # Log cleanup errors if any (in a real scenario, you might want to log these)
        if cleanup_errors:
            print(f"Cleanup warnings: {cleanup_errors}")
        
        return cleanup_errors