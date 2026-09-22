# SleekFlow Playwright Automation Test

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-45ba4b?style=flat&logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/Pytest-Framework-0A9EDC?style=flat&logo=pytest&logoColor=white)](https://pytest.org)
[![SleekFlow Playwright Automation Test](https://img.shields.io/badge/SleekFlow-Playwright%20Automation%20Test-6C2DC7?style=flat)](https://github.com/techtimemaniac/sleekflow-playwright-python)

A production-ready test automation framework built with **Playwright** and **Python**, implementing industry best practices including Page Object Model, parallel execution, and CI/CD integration.

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Page Object Model** | Clean separation of test logic and page interactions |
| **Multi-Browser** | Chromium, Firefox, WebKit support |
| **Parallel Execution** | pytest-xdist for faster test runs |
| **CI/CD Ready** | GitHub Actions workflow included |
| **Rich Reporting** | Allure reports, HTML reports, screenshots, videos |
| **Data-Driven** | JSON, YAML test data support |
| **Type Hints** | Full annotations for IDE support |

## 🏗️ Project Structure

```
sleekflow-playwright-python/
├── pages/                    # Page Object Models
│   ├── base_page.py         # Base class with common methods
│   ├── sleekflow_auth_page.py
│   ├── sleekflow_login_page.py
│   └── sleekflow_signup_page.py
├── tests/                    # Test suites
│   ├── test_sleekflow_login_smoke.py
│   ├── test_sleekflow_login.py
│   └── test_sleekflow_signup.py
├── utils/                    # Utilities
│   ├── config_reader.py     # Configuration management
│   ├── logger.py            # Custom logging
│   └── helpers.py           # Helper functions
├── test_data/               # Test data files
├── .github/workflows/       # CI/CD pipelines
├── conftest.py              # Pytest fixtures
├── pytest.ini               # Pytest configuration
└── requirements.txt         # Dependencies
```

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/techtimemaniac/sleekflow-playwright-python.git
cd sleekflow-playwright-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
playwright install

# Run tests
pytest
```

## 🧪 Running Tests

```bash
# All tests
pytest

# Specific markers
pytest -m smoke
pytest -m regression

# Parallel execution
pytest -n auto

# Specific browser
pytest --browser firefox

# With Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## ⚙️ Configuration

Environment variables (`.env`):

```env
BASE_URL=https://app.sleekflow.io
BROWSER=chromium
HEADLESS=true
SLEEKFLOW_LOGIN_USERNAME=
SLEEKFLOW_LOGIN_PASSWORD=
SLEEKFLOW_SIGNUP_USERNAME=
SLEEKFLOW_SIGNUP_PASSWORD=
```

## 📝 Writing Tests

```python
import pytest
from pages.automation_page import SleekFlowAutomationPage

@pytest.mark.smoke
def test_user_login(page):
    auth = SleekFlowAutomationPage(page)
    auth.open_login()
    assert auth.is_visible(auth.EMAIL_INPUT)
```

## 📊 Reports

| Report Type | Location |
|-------------|----------|
| HTML Report | `reports/html/report.html` |
| Allure Report | `reports/allure-results/` |
| Logs | `logs/test_execution.log` |

## 🔄 CI/CD

Tests run automatically on:
- Push to `main`/`develop` branches
- Pull requests
- Scheduled nightly runs

## 👤 Author

**Dharna Johari**
