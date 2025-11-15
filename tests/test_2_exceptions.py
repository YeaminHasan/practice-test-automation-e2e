import pytest
from playwright.sync_api import Page, expect , TimeoutError as PlaywrightTimeoutError

BASE_URL = "https://practicetestautomation.com/practice-test-exceptions/"

def click_add(page: Page):page.locator("//button[@id='add_btn']").click()
def second_row_input(page: Page):return page.locator("input").nth(1)
def save_button_visible(page: Page): return page.locator('[name="Save"]:visible')


def test_no_such_element_with_wait(page: Page): #TestCase 1
    """Test case 1: Wait for Row 2 to appear to avoid NoSuchElementException.
    Without the explicit wait the test would fail with a NoSuchElementException
    because Row 2 appears asynchronously."""

    page.goto(BASE_URL)
    click_add(page)
    second = second_row_input(page)
    second.wait_for(state="visible", timeout=7000)
    assert second.is_visible()


def test_element_not_interactable_and_save(page: Page): #TestCase 2
    """Test case 2: Type into second input and click the visible Save button.
    The page contains two elements with name="Save"; the first one is
    invisible. Clicking the invisible one would cause an ElementNotInteractable
    error. We explicitly target the visible Save button."""

    page.goto(BASE_URL)
    click_add(page)
    second = second_row_input(page)
    second.wait_for(state="visible", timeout=7000)
    second.fill("My favorite food")
    save_button_visible(page).click() # visible Save button
    page.locator("//button[@id='edit_btn']").nth(1).wait_for(state="visible", timeout=5000)
    expect(page.get_by_role("textbox").nth(1)).to_have_value("My favorite food")


def test_invalid_element_state_enable_edit_and_type(page: Page): #TestCase 3
    """Test case 3: Enable editing and change the input value.
    The input is disabled initially; attempting to clear or type into it will
    raise an exception. Click the Edit control first, then type and verify."""

    page.goto(BASE_URL)
    # Find the (first) input and the Edit button; enable editing first
    input_field = page.locator("input").first
    page.locator("//button[@id='edit_btn']").click()
    input_field.fill("Editable now")
    assert input_field.input_value() == "Editable now"


def test_stale_element_reference_behavior(page: Page): #TestCase 4
    """Test case 4: Confirm an element becomes detached after adding a row.
    In Selenium or Playwright this causes StaleElementReferenceException. Here we assert the
    original instructions element is no longer attached after clicking Add."""

    page.goto(BASE_URL)
    instructions_text_element = page.locator("text=Push “Add” button to add another row")
    click_add(page)
    assert not instructions_text_element.is_visible()


def test_timeout_exception_demo(page: Page): #TestCase 5
    """Test case 5: Demonstrate a timeout when waiting too briefly for Row 2.

    The row appears after ~5s on the demo page; waiting only 3s should raise
    a Playwright TimeoutError. We assert that the timeout occurs to document
    the behavior without making the test suite unexpectedly fail."""
    page.goto(BASE_URL)
    click_add(page)

    second = second_row_input(page)
    with pytest.raises(PlaywrightTimeoutError):
        second.wait_for(state="visible", timeout=3000)

