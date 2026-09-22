# ✅ Framework Setup & Usage Checklist

## 📋 Initial Setup (One-Time)

### Step 1: Prerequisites
- [ ] Python 3.10+ installed
- [ ] pip installed
- [ ] Git installed (optional, for version control)
- [ ] VS Code/Intellij installed (recommended)

### Step 2: Automated Setup
**Windows:**
```powershell
cd "c:\Users\user\Work\sleekflow"
.\setup.bat
```

**What this does:**
- ✅ Installs all Python dependencies
- ✅ Installs Playwright browsers (Chromium, Firefox, WebKit)
- ✅ Creates necessary directories (logs, reports, screenshots, etc.)
- ✅ Sets up .env file from .env.example

### Step 3: Verify Installation
```powershell
# Check pytest is installed
pytest --version

# Check playwright is installed
playwright --version

# List installed browsers
playwright install --help
```

---

## 🚀 Running Tests

### Quick Commands Reference

```powershell
# 1. Run smoke tests (fastest, critical tests only)
pytest -m smoke

# 2. Run smoke tests in headed mode (see browser)
pytest -m smoke --headed

# 3. Run all tests
pytest

# 4. Run regression tests
pytest -m regression

# 5. Run tests in parallel (4 workers)
pytest -n 4

# 6. Run with specific browser
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit

# 7. Run specific test file
pytest -m smoke

# 8. Run specific test class
pytest tests/test_sleekflow_login_smoke.py -m smoke

# 9. Run specific test
pytest tests/test_sleekflow_login_smoke.py::TestSleekFlowLoginSmoke::test_login_page_is_ready

# 10. Run with verbose output
pytest -v

# 11. Run with extra verbose output
pytest -vv

# 12. Run and stop on first failure
pytest -x

# 13. Run and stop after 3 failures
pytest --maxfail=3

# 14. Run in headed mode with slow motion
pytest --headed --slowmo=1000

# 15. Generate Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 📊 Viewing Reports

### HTML Report (Simple)
```powershell
# After running tests, open:
start reports/html/report.html
```

### Allure Report (Rich, Interactive)
```powershell
# Generate and view
allure serve reports/allure-results

# Or generate static report
allure generate reports/allure-results -o reports/allure-report --clean
start reports/allure-report/index.html
```

### Logs
```powershell
# View latest log file
notepad logs/test_execution_<date>.log
```

### Failure Artifacts
- **Screenshots**: `screenshots/`
- **Videos**: `videos/`
- **Traces**: `traces/` (view with `playwright show-trace <file>.zip`)

---

## 🔧 Configuration

### Edit .env File
```powershell
notepad .env
```

**Key Settings:**
```ini
# Change browser
BROWSER=chromium  # or firefox, webkit

# Run in headless mode
HEADLESS=true     # or false to see browser

# Adjust timeouts (milliseconds)
DEFAULT_TIMEOUT=30000
NAVIGATION_TIMEOUT=30000

# Enable/disable features
SCREENSHOT_ON_FAILURE=true
VIDEO_ON_FAILURE=true
TRACE_ON_FAILURE=true

# Parallel execution
MAX_WORKERS=4
```

---

## 📝 Writing New Tests

### 1. Create Test File
```python
# tests/test_new_feature.py
import pytest
from pages.automation_page import SleekFlowAutomationPage

@pytest.mark.smoke  # or @pytest.mark.regression
class TestNewFeature:
    def test_example(self, page, base_url):
        # Arrange
        automation_page = AutomationPage(page, base_url)
        
        # Act
        automation_page.navigate()
        automation_page.click(automation_page.SOME_BUTTON)
        
        # Assert
        assert automation_page.is_visible(automation_page.SOME_ELEMENT)
```

### 2. Run Your New Test
```powershell
pytest tests/test_new_feature.py -v
```

---

## 🎯 Common Test Scenarios

### Test 1: Verify Page Loads
```python
def test_page_loads(self, page, base_url):
    automation_page = AutomationPage(page, base_url)
    automation_page.navigate()
    automation_page.verify_page_loaded()
```

### Test 2: Fill and Submit Form
```python
def test_form_submission(self, page, base_url):
    automation_page = AutomationPage(page, base_url)
    automation_page.navigate()
    automation_page.fill_contact_form("John Doe", "Test message", "5")
    automation_page.submit_form()
```

### Test 3: Navigate and Verify
```python
def test_navigation(self, page, base_url):
    automation_page = AutomationPage(page, base_url)
    automation_page.navigate()
    automation_page.click_fake_landing_page()
    assert "landing" in automation_page.get_url().lower()
```

---

## 🐛 Debugging

### View Trace File
```powershell
# After test failure, a trace file is saved
playwright show-trace traces/<test_name>_<timestamp>.zip
```

### Run Single Test with Debug
```powershell
pytest tests/test_sleekflow_login_smoke.py::TestSleekFlowLoginSmoke::test_login_page_is_ready -v -s --headed
```

### Use VS Code Debugger
1. Open `test_sleekflow_login_smoke.py`
2. Set breakpoint
3. Press F5 or use Debug menu
4. Select "Python: Pytest - Current File"

---

## 📦 Adding New Page Objects

### 1. Create Page File
```python
# pages/new_page.py
from pages.base_page import BasePage
from playwright.sync_api import Page

class NewPage(BasePage):
    # Locators
    HEADER = "h1"
    BUTTON = "button#submit"
    
    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page)
        self.base_url = base_url or "https://example.com"
    
    def navigate(self) -> 'NewPage':
        super().navigate(self.base_url)
        return self
    
    def click_submit(self) -> 'NewPage':
        self.click(self.BUTTON)
        return self
```

### 2. Use in Tests
```python
from pages.new_page import NewPage

def test_new_page(self, page):
    new_page = NewPage(page)
    new_page.navigate().click_submit()
```

---

## 🔄 CI/CD

### GitHub Actions (Already Configured)
```yaml
# .github/workflows/test.yml is ready
# Just push to GitHub and tests run automatically
```

**What runs automatically:**
- ✅ All tests on every push
- ✅ Multi-browser testing
- ✅ Multi-OS testing
- ✅ Automatic report generation
- ✅ Artifact uploads

---

## 📈 Best Practices Checklist

### Test Writing
- [ ] Use descriptive test names
- [ ] One test = one scenario
- [ ] Use appropriate markers (@pytest.mark.smoke, etc.)
- [ ] Use Page Objects (don't write locators in tests)
- [ ] Add proper assertions
- [ ] Add logging for important steps

### Code Quality
- [ ] Use type hints
- [ ] Add docstrings
- [ ] Follow naming conventions
- [ ] Don't hardcode values (use config/test data)
- [ ] Handle errors gracefully

### Maintenance
- [ ] Keep dependencies updated
- [ ] Review and clean up old screenshots/videos
- [ ] Update documentation
- [ ] Review and fix flaky tests
- [ ] Monitor test execution time

---

## 🆘 Troubleshooting

### Issue: Playwright not found
**Solution:**
```powershell
python -m playwright install
```

### Issue: Tests failing with timeout
**Solution:**
1. Increase timeout in `.env`:
   ```ini
   DEFAULT_TIMEOUT=60000
   ```
2. Or use headed mode to see what's happening:
   ```powershell
   pytest --headed --slowmo=500
   ```

### Issue: Browser not launching
**Solution:**
```powershell
# Reinstall browsers
playwright install --force
```

### Issue: Import errors
**Solution:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: No module named 'pytest'
**Solution:**
```powershell
# Use full Python path
C:/Users/user/AppData/Local/Python/pythoncore-3.14-64/python.exe -m pip install pytest
```

---

## 📚 Learning Path

### Beginner
1. ✅ Run smoke tests: `pytest -m smoke --headed`
2. ✅ View HTML report
3. ✅ Read QUICKSTART.md
4. ✅ Modify existing test

### Intermediate
1. ✅ Create new test file
2. ✅ Use Page Objects
3. ✅ Run tests in parallel
4. ✅ View Allure reports
5. ✅ Debug with traces

### Advanced
1. ✅ Create new Page Object
2. ✅ Add custom utilities
3. ✅ Configure CI/CD
4. ✅ Implement data-driven tests
5. ✅ Cross-browser testing

---

## ✅ Daily Workflow

### Morning Routine
```powershell
# 1. Pull latest changes (if using Git)
git pull

# 2. Run smoke tests
pytest -m smoke

# 3. Check reports
start reports/html/report.html
```

### Before Commit
```powershell
# 1. Run all tests
pytest

# 2. Check for failures
# 3. Review screenshots/logs if any failures
# 4. Fix issues
# 5. Rerun tests
pytest

# 6. Commit
git add .
git commit -m "Your message"
git push
```

### End of Day
```powershell
# 1. Run full regression
pytest -m regression

# 2. Generate Allure report
allure serve reports/allure-results

# 3. Review results
# 4. Document any issues
```

---

## 🎓 Quick Reference

### Test Markers
- `@pytest.mark.smoke` - Quick validation
- `@pytest.mark.regression` - Full test suite
- `@pytest.mark.critical` - Must pass tests
- `@pytest.mark.ui` - UI tests
- `@pytest.mark.slow` - Long-running tests

### Fixtures Available
- `page` - Playwright page instance
- `base_url` - Base URL from config
- `context` - Browser context
- `browser` - Browser instance

### Important Files
- `pytest.ini` - Pytest configuration
- `.env` - Environment variables
- `conftest.py` - Test fixtures
- `requirements.txt` - Dependencies

---

**🎉 You're all set! Start testing with:**
```powershell
pytest -m smoke --headed
```
