# Graduation Project. Assignment 2: API Tests

Automated API tests for the Stellar Burgers burger ordering service.

---

## 📁 Project Structure

```text
tests/              # Pytest test modules for each feature
                    # Example: user login, logout, order creation, etc.

utils/              # Utility modules
                    # Includes API endpoint URLs and test data generators

requirements.txt    # Python dependencies

pytest.ini          # Pytest configuration

README.md           # Project documentation and usage instructions
```

---

## 🚀 Installation

Install project dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running Tests

Run all API tests using Pytest:

```bash
pytest tests/ -v --tb=short --alluredir=allure-results
```

---

## 📊 Allure Report

Generate and open the Allure report:

```bash
allure serve allure-results
```

---

## ✅ Tested Features

- User registration
- User login
- User logout
- Creating orders
- Retrieving user orders
- Authorization validation
- API response validation

---

## 🛠 Technologies

- Python
- pytest
- requests
- allure-pytest

---

## 👩‍💻 Author

Natalia Kozit  
QA Automation Engineer

GitHub: [@natyko](https://github.com/natyko)

---

## 📌 About

API automated testing project for the Stellar Burgers service using Python, Pytest, Requests, and Allure Report.
