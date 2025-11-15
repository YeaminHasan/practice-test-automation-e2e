import pytest

BASE_URL = "https://practicetestautomation.com/practice-test-login/"


def test_login_positive(page): #TestCase 1
    """Positive login: correct username and password should succeed."""
    page.goto(BASE_URL)
    # fill form
    page.fill("#username", "student")
    page.fill("#password", "Password123")
    page.click("#submit")
    # assertions: URL and content
    assert "practicetestautomation.com/logged-in-successfully" in page.url
    content = page.text_content("body") or ""
    assert "Congratulations" in content or "successfully logged in" in content.lower()
    assert page.is_visible("text=Log out")


def test_login_negative_username(page): #TestCase 2
    """Negative test: invalid username shows correct error message."""
    page.goto(BASE_URL)
    page.fill("#username", "incorrectUser")
    page.fill("#password", "Password123")
    page.click("#submit")
    assert page.is_visible("#error")
    assert page.text_content("#error").strip() == "Your username is invalid!"


def test_login_negative_password(page): #TestCase 3
    """Negative test: invalid password shows correct error message."""
    page.goto(BASE_URL)
    page.fill("#username", "student")
    page.fill("#password", "incorrectPassword")
    page.click("#submit")
    assert page.is_visible("#error")
    assert page.text_content("#error").strip() == "Your password is invalid!"
