import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    """Launch one browser per test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        yield browser
        browser.close()


@pytest.fixture(scope="module")
def context(browser):
    """Create a browser context per test module with geolocation permissions."""
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    yield context
    context.close()


@pytest.fixture(scope="module")
def page(context):
    """Open a new page for each test module."""
    page = context.new_page()
    yield page
    page.close()