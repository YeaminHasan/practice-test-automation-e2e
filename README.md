**Practice Test Automation — E2E**

- **Purpose**: This repository contains Playwright end-to-end tests (Python) that exercise several demo pages on Practicetestautomation.com. The tests demonstrate login flows, common web exceptions (useful for learning Selenium/Playwright error handling), and table/filter/sort behaviors.

**Quick Summary**
- **Language**: Python
- **Test runner**: pytest
- **Browser automation**: Playwright (sync API)
- **Fixtures**: `conftest.py` provides `browser`, `context` (viewport set to 1280x720), and `page` fixtures.

**Repository Layout**
- `conftest.py`: Playwright fixtures and browser/context setup
- `requirements.txt`: Python dependencies
- `tests/`
	- `test_1_login.py`: login positive/negative tests
	- `test_2_exceptions.py`: examples of NoSuchElement, ElementNotInteractable, InvalidElementState, StaleElementReference, Timeout behaviors
	- `test_3_table.py`: table filtering, sorting and reset behavior tests

**Prerequisites**
- Python 3.8+ installed
- `pip` available
- (Optional) A virtual environment tool such as `venv`

Windows notes:
- On Windows use PowerShell or CMD. Commands below show both PowerShell and CMD variants where they differ.

**Setup — Step by step**
1. Clone the repository:

```bash
git clone https://github.com/YeaminHasan/practice-test-automation-e2e.git
cd practice-test-automation-e2e
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
# PowerShell (may require changing execution policy):
.
\venv\Scripts\Activate.ps1
```

Windows (CMD):

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
or
pip install --break-system-packages -r requirements.txt
```

Windows users: the same `pip` commands apply once the virtual environment is activated. If you see permission errors, run the terminal as Administrator or use the virtual environment's `pip` directly (`venv\Scripts\pip.exe install -r requirements.txt`).

4. Install Playwright browsers (required the first time):

```bash
playwright install
```

Windows: run the same `playwright install` command. If you're using PowerShell and installed Playwright in a virtual environment, use the venv pip/shim (`venv\Scripts\playwright.cmd install`).

Notes on `playwright install --with-deps`:
- The `--with-deps` option is useful on Linux CI runners to install OS-level dependencies. It is not required on most Windows developer machines and may not be supported identically on Windows.

Notes: If `playwright` is not found, ensure `pip` installed the package from `requirements.txt` and that the virtual environment is activated.

**How to run tests**
- Run the whole test suite:

```bash
pytest -q
```

Windows (PowerShell/CMD):

```powershell
pytest -q
```

- Run a single test file:

```bash
pytest tests/test_2_exceptions.py -q
```

- Run a specific test function (useful while developing):

```bash
pytest tests/test_2_exceptions.py::test_timeout_exception_demo -q
```

Windows (PowerShell/CMD): same command applies once the virtual environment is activated.

**Configuration & Tips**
- The `conftest.py` file currently launches Chromium with `headless=False` and `slow_mo=500` to make runs visible while developing. For CI or faster runs, change `headless=True` and remove `slow_mo`.
- The browser context created by the `context` fixture sets a viewport of `1280x720`. If you need different dimensions for responsive testing, update `conftest.py` or add an environment-driven configuration.
- Tests include small explicit waits (`page.wait_for_timeout(...)`) to allow the demo pages to update. If you see flaky failures, increase the timeout or replace with smarter `locator.wait_for(...)` calls.

Windows-specific tips:
- Execution policy: PowerShell may block script execution by default. If you see `Activate.ps1` blocked errors, run PowerShell as Administrator and run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`, or use the CMD `activate.bat` instead.
- Long paths: on older Windows installations long file paths may be disabled; enable them or keep repository path short to avoid path length issues.

**CI / GitHub Actions (suggested)**
Create a `.github/workflows/ci.yml` with steps similar to:

```yaml
name: Python Playwright Tests

on: [push, pull_request]

jobs:
	test:
		runs-on: ubuntu-latest
		steps:
			- uses: actions/checkout@v4
			- name: Set up Python
				uses: actions/setup-python@v4
				with:
					python-version: '3.10'
			- name: Install dependencies
				run: |
					python -m pip install --upgrade pip
					pip install -r requirements.txt
					playwright install --with-deps
			- name: Run tests
				run: pytest -q
```

**Common Troubleshooting**
- Playwright browsers missing: run `playwright install` and ensure network access.
- Tests fail due to timing: increase explicit timeouts or use `locator.wait_for(state=...)`/`expect(...)` for element-aware waits.
- Virtualenv not activated: ensure `source venv/bin/activate` before `pip install` and running tests.

**Contributing**
- PRs welcome. Please keep tests focused and deterministic. When adding new tests, prefer locators and `expect` assertions instead of brittle fixed indexing.

**License & Attribution**
- This repository is provided as-is for learning and demonstration purposes. Add a license file if you plan to open-source it publicly.

---

If you want, I can also:
- Add a GitHub Actions workflow file for CI
- Toggle `conftest.py` to use `headless` mode by default for CI
- Add a short CONTRIBUTING.md with contribution guidelines

If you'd like one of those, tell me which and I'll add it.
