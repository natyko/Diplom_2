import uuid


def generate_unique_user():
    """Generate a unique user payload with random email and name."""
    unique_id = uuid.uuid4().hex  # random unique string
    email = f"testuser_{unique_id[:8]}@yopmail.com"
    password = "P@ssw0rd!"  # a constant or could be randomized as well
    name = "User" + unique_id[:5]
    return {"email": email, "password": password, "name": name}
