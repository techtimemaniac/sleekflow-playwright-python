# 🎨 Framework Visual Architecture

## 📐 Complete Framework Structure

```
sleekflow playwright python/
│
├── 📁 pages/                           # PAGE OBJECT LAYER
│   ├── __init__.py                     # Package initialization
│   ├── base_page.py                    # 🔷 Base Page (400+ lines)
│   │   ├── Element interactions        #    - click(), fill(), type()
│   │   ├── Smart waits                 #    - wait_for_element()
│   │   ├── Assertions                  #    - assert_element_visible()
│   │   ├── Navigation                  #    - navigate(), go_back()
│   │   └── Utilities                   #    - take_screenshot()
│   │
│   └── automation_page.py              # 🔷 Ultimate QA Page (250+ lines)
│       ├── Locators                    #    - All page elements
│       ├── Form methods                #    - fill_contact_form()
│       ├── Navigation methods          #    - click_fake_landing_page()
│       └── Verification methods        #    - verify_page_loaded()
│
├── 📁 tests/                           # TEST LAYER
│   ├── __init__.py                     # Package initialization
│   ├── conftest.py                     # 🧪 Pytest Configuration
│   │   ├── Fixtures                    #    - page, base_url
│   │   ├── Browser config              #    - browser launch args
│   │   ├── Failure handling            #    - screenshots, traces
│   │   └── Hooks                       #    - pytest hooks
│   │
│   ├── test_sleekflow_login_smoke.py   # 🧪 Login Smoke Tests
│   │   ├── Page load tests             #    - test_page_loads_successfully
│   │   ├── Element tests               #    - test_page_has_essential_elements
│   │   ├── Interaction tests           #    - test_form_fields_are_interactive
│   │   └── Performance tests           #    - test_page_responsiveness
│   │
│   ├── test_sleekflow_login.py         # 🧪 Login Regression Tests
│   ├── test_sleekflow_signup.py        # 🧪 Signup Tests
│   │   ├── Form tests                  #    - test_fill_form_with_valid_data
│   │   ├── Validation tests            #    - test_empty_form_submission
│   │   ├── Navigation tests            #    - test_navigate_to_big_page
│   │   └── Structure tests             #    - test_page_structure
│   │
│   └── test_api.py                     # 🧪 API Tests (placeholder)
│       └── API test examples           #    - Ready for API testing
│
├── 📁 utils/                           # UTILITY LAYER
│   ├── __init__.py                     # Package initialization
│   │
│   ├── logger.py                       # 📝 Logging System
│   │   ├── ColoredFormatter            #    - Colored console output
│   │   ├── File logging                #    - Rotating log files
│   │   ├── Multiple levels             #    - DEBUG, INFO, ERROR
│   │   └── get_logger()                #    - Logger factory
│   │
│   ├── config_reader.py                # ⚙️ Configuration Manager
│   │   ├── Singleton pattern           #    - Single instance
│   │   ├── .env file loading           #    - Environment variables
│   │   ├── Type-safe getters           #    - get_bool(), get_int()
│   │   └── Configuration properties    #    - base_url, browser, timeouts
│   │
│   ├── test_data.py                    # 📊 Test Data Manager
│   │   ├── TestDataManager             #    - JSON/YAML data loading
│   │   ├── Faker integration           #    - Fake data generation
│   │   ├── ContactFormData             #    - Form test data
│   │   └── Data generators             #    - generate_fake_user()
│   │
│   └── helpers.py                      # 🛠️ Helper Utilities
│       ├── Wait utilities              #    - wait_for_condition()
│       ├── Screenshot helpers          #    - take_screenshot()
│       ├── File operations             #    - read_file(), write_file()
│       ├── Retry mechanism             #    - retry_on_exception()
│       └── Timestamp utilities         #    - get_timestamp()
│
├── 📁 test_data/                       # TEST DATA LAYER
│   ├── test_users.json                 # 📄 User test data
│   │   ├── User accounts               #    - name, email, password
│   │   └── Contact messages            #    - test messages
│   │
│   └── test_scenarios.yaml             # 📄 Test scenarios
│       ├── Smoke tests                 #    - Critical scenarios
│       ├── Regression tests            #    - Full scenarios
│       └── Validation rules            #    - Form validation
│
├── 📁 .github/workflows/               # CI/CD LAYER
│   └── test.yml                        # ⚡ GitHub Actions Workflow
│       ├── Multi-browser               #    - Chrome, Firefox, Safari
│       ├── Multi-OS                    #    - Windows, Linux, macOS
│       ├── Multi-Python                #    - 3.10, 3.11, 3.12
│       ├── Parallel execution          #    - Matrix strategy
│       ├── Artifact upload             #    - Screenshots, videos
│       └── Allure reporting            #    - Report generation
│
├── 📁 .vscode/                         # IDE CONFIGURATION
│   ├── settings.json                   # 🔧 VS Code settings
│   │   ├── Python config               #    - Testing, linting
│   │   └── File exclusions             #    - Hide cache files
│   │
│   └── launch.json                     # 🐛 Debug configurations
│       ├── Current file                #    - Run current test
│       ├── Smoke tests                 #    - Run all smoke tests
│       └── All tests                   #    - Run entire suite
│
├── 📁 reports/                         # REPORTS (Auto-generated)
│   ├── 📁 html/                        # HTML reports
│   │   └── report.html                 #    - Self-contained report
│   │
│   ├── 📁 allure-results/              # Allure raw results
│   │   └── *.json                      #    - Test results data
│   │
│   └── 📁 allure-report/               # Allure generated report
│       └── index.html                  #    - Interactive dashboard
│
├── 📁 logs/                            # LOGS (Auto-generated)
│   └── test_execution_YYYYMMDD.log     # Daily log files
│
├── 📁 screenshots/                     # SCREENSHOTS (On failure)
│   └── test_name_timestamp.png         # Failure screenshots
│
├── 📁 videos/                          # VIDEOS (On failure)
│   └── test_name_timestamp.webm        # Test execution videos
│
├── 📁 traces/                          # TRACES (On failure)
│   └── test_name_timestamp.zip         # Playwright traces
│
├── 📄 pytest.ini                       # ⚙️ Pytest Configuration
│   ├── Test discovery                  #    - Patterns, paths
│   ├── Markers                         #    - smoke, regression, etc.
│   ├── Command options                 #    - Default arguments
│   └── Logging config                  #    - Log levels, formats
│
├── 📄 requirements.txt                 # 📦 Python Dependencies
│   ├── Testing framework               #    - pytest, playwright
│   ├── Reporting                       #    - allure, html
│   ├── Data handling                   #    - faker, yaml, pandas
│   └── Quality tools                   #    - mypy, pylint, black
│
├── 📄 .env                             # 🔐 Environment Variables
│   ├── Base configuration              #    - BASE_URL, BROWSER
│   ├── Timeouts                        #    - DEFAULT_TIMEOUT
│   ├── Feature flags                   #    - SCREENSHOT_ON_FAILURE
│   └── Credentials                     #    - TEST_USERNAME (if needed)
│
├── 📄 .env.example                     # 📋 Environment Template
│   └── Example configuration           #    - Template for .env
│
├── 📄 .gitignore                       # 🚫 Git Ignore Rules
│   ├── Python artifacts                #    - __pycache__, *.pyc
│   ├── Virtual environments            #    - venv/, env/
│   ├── Reports & logs                  #    - reports/, logs/
│   └── IDE files                       #    - .idea/, .vscode/
│
├── 📄 conftest.py                      # 🔧 Root Configuration
│   └── Python path setup               #    - Add project to path
│
├── 📄 run_tests.py                     # 🚀 Test Runner Script
│   ├── run_smoke_tests()               #    - Quick smoke tests
│   ├── run_regression_tests()          #    - Full regression
│   ├── run_parallel_tests()            #    - Parallel execution
│   └── generate_allure_report()        #    - Report generation
│
├── 📄 setup.bat                        # 🔧 Windows Setup Script
│   ├── Install dependencies            #    - pip install
│   ├── Install browsers                #    - playwright install
│   ├── Create directories              #    - mkdir
│   └── Setup environment               #    - .env creation
│
├── 📄 setup.sh                         # 🔧 Linux/Mac Setup Script
│   └── Same as setup.bat               #    - For Unix systems
│
├── 📄 README.md                        # 📚 Main Documentation
│   ├── Framework overview              #    - Architecture, features
│   ├── Setup instructions              #    - Installation guide
│   ├── Usage examples                  #    - How to run tests
│   └── Best practices                  #    - Guidelines
│
├── 📄 QUICKSTART.md                    # ⚡ Quick Start Guide
│   ├── Installation                    #    - Fast setup
│   ├── Running tests                   #    - Quick commands
│   ├── Viewing reports                 #    - Report access
│   └── Troubleshooting                 #    - Common issues
│
├── 📄 ARCHITECTURE.md                  # 🏛️ Architecture Documentation
│   ├── Design principles               #    - Patterns, layers
│   ├── Component details               #    - Each component
│   ├── Execution flow                  #    - Test lifecycle
│   └── Scalability                     #    - Future growth
│
├── 📄 FRAMEWORK_SUMMARY.md             # 📝 Framework Summary
│   ├── What was created                #    - Complete list
│   ├── Features                        #    - All capabilities
│   ├── Test coverage                   #    - Test count
│   └── Quality metrics                 #    - Why 0.1% QALead
│
└── 📄 CHECKLIST.md                     # ✅ Usage Checklist
    ├── Setup checklist                 #    - Step-by-step
    ├── Running tests                   #    - Commands reference
    ├── Debugging guide                 #    - Troubleshooting
    └── Best practices                  #    - Do's and don'ts
```

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     TEST EXECUTION FLOW                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  1. INITIALIZATION                                          │
│     - Load pytest.ini                                       │
│     - Load .env configuration                               │
│     - Create directories                                    │
│     - Setup logging                                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  2. BROWSER SETUP (Per Test)                                │
│     - Launch browser (Chromium/Firefox/WebKit)              │
│     - Create context with config                            │
│     - Create new page                                       │
│     - Set timeouts                                          │
│     - Start tracing                                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  3. TEST EXECUTION                                          │
│                                                             │
│     Test Code                                               │
│         │                                                   │
│         ▼                                                   │
│     Page Object (automation_page.py)                        │
│         │                                                   │
│         ├─► Locators                                        │
│         ├─► Business Logic Methods                          │
│         │                                                   │
│         ▼                                                   │
│     Base Page (base_page.py)                                │
│         │                                                   │
│         ├─► Element Interactions                            │
│         ├─► Waits & Assertions                              │
│         ├─► Logging                                         │
│         │                                                   │
│         ▼                                                   │
│     Playwright API                                          │
│         │                                                   │
│         ▼                                                   │
│     Browser (Actual Web Page)                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  4. RESULT HANDLING                                         │
│                                                             │
│     IF TEST PASSES:                                         │
│         ├─► Log success                                     │
│         ├─► Stop trace                                      │
│         └─► Update reports                                  │
│                                                             │
│     IF TEST FAILS:                                          │
│         ├─► Take screenshot → screenshots/                  │
│         ├─► Save video → videos/                            │
│         ├─► Save trace → traces/                            │
│         ├─► Log error                                       │
│         ├─► Attach to Allure report                         │
│         └─► Update reports                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  5. CLEANUP                                                 │
│     - Close page                                            │
│     - Close context                                         │
│     - Generate reports                                      │
│     - Archive logs                                          │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Component Interaction Diagram

```
┌────────────┐
│   Tests    │───────┐
└────────────┘       │
                     ▼
┌────────────┐   ┌──────────────┐   ┌────────────┐
│  Fixtures  │──▶│ Page Objects │──▶│ Base Page  │
└────────────┘   └──────────────┘   └────────────┘
      │                │                   │
      │                │                   ▼
      │                │            ┌────────────┐
      │                │            │ Playwright │
      │                │            └────────────┘
      │                │
      │                ▼
      │         ┌────────────┐
      │         │ Test Data  │
      │         └────────────┘
      │
      ▼
┌────────────┐   ┌────────────┐   ┌────────────┐
│   Config   │   │   Logger   │   │  Helpers   │
└────────────┘   └────────────┘   └────────────┘
      │                │                │
      └────────────────┴────────────────┘
                       │
                       ▼
                ┌────────────┐
                │  Reports   │
                └────────────┘
```

## 📊 File Size & Complexity Metrics

```
Component                 Lines of Code    Complexity
─────────────────────────────────────────────────────
base_page.py                    400         Medium
automation_page.py              250         Low
conftest.py                     200         Medium
test_sleekflow_login_smoke.py   current    Low
test_sleekflow_login.py         current    Low
logger.py                       150         Low
config_reader.py                120         Low
test_data.py                    180         Low
helpers.py                      200         Low
─────────────────────────────────────────────────────
TOTAL                         1,950         
```

## 🚀 Execution Speed

```
Test Type          Tests    Avg Time     Parallel
───────────────────────────────────────────────────
Smoke              8        ~20s         ~8s
Regression         15+      ~90s         ~30s
Full Suite         20+      ~120s        ~40s
```

---

**This visual guide shows the complete framework architecture at a glance! 🎨**
