# Stellar Burgers API Test Suite

Automated API tests for the Stellar Burgers burger ordering service — a multi-page web app with authentication, order management, and user profiles.

**Tech:** Python · Pytest · requests · conftest fixtures · parametrized test data

## Coverage


User authentication: registration, login, logout, token refresh
User profile: data retrieval and updates  
Order creation: authenticated and unauthenticated flows
Order history: retrieval per user
Negative paths: invalid credentials, missing tokens, malformed payloads


## Project Structure

```
tests/         # Pytest test modules organized by feature (auth, orders, profile)
utils/         # Reusable API client + test data generators
conftest.py    # Shared fixtures (user creation, token management, cleanup)
pytest.ini     # Pytest configuration
requirements.txt
```

## Design Notes


**API client abstraction** — endpoint URLs and request logic isolated in `utils/`, keeping tests focused on behavior, not transport.
**Fixture-driven setup/teardown** — each test gets a fresh authenticated user; cleanup runs automatically.
**Parametrized test data** — negative paths covered without test duplication.


## Run

```bash
pip install -r requirements.txt
pytest tests/ -v
```
