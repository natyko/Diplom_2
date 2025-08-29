Дипломный проект. Задание 2: API-тесты
Автотесты для проверки API сервиса заказа бургеров — Stellar Burgers

Структура проекта

tests/ – Contains Pytest test modules for each feature (user logout, login, etc.)
utils/ – Utility modules (for API endpoint URLs and test data generation)
requirements.txt – Python dependencies
pytest.ini – Pytest configuration
README.md – Usage instructions


Установка зависимостей:
```bash
 pip install -r requirements.txt 
```
Execute the tests using Pytest:
```bash
pytest tests/ -v --tb=short --alluredir=allure-results
```
Generating Allure Report:
```bash
allure serve allure-results
```



