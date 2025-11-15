from playwright.sync_api import Page, expect
import pytest
BASE_URL = "https://practicetestautomation.com/practice-test-table/"

def test_language_filter_java(page: Page): #TestCase 1
    page.goto(BASE_URL)
    # Select Language = Java
    page.locator("label").filter(has_text="Java").click()
    # Verify that only Java courses are visible
    expect(page.get_by_role("cell", name="Java").first).to_be_visible()
    expect(page.get_by_role("cell", name="Java").nth(2)).to_be_visible()
    expect(page.get_by_role("cell", name="Java").nth(3)).to_be_visible()
    expect(page.get_by_role("cell", name="Java").nth(4)).to_be_visible()
    expect(page.get_by_role("cell", name="Java").nth(5)).to_be_visible()


def test_level_filter_beginner(page: Page): ##TestCase 2
    page.goto(BASE_URL)
    # Uncheck Intermediate and Advanced
    page.locator("label").filter(has_text="Intermediate").click()
    page.locator("label").filter(has_text="Advanced").click()
    # Verify that only Beginner courses are visible
    expect(page.get_by_role("cell", name="Beginner").first).to_be_visible()
    expect(page.get_by_role("cell", name="Beginner").nth(1)).to_be_visible()


def test_min_enrollments_10000(page: Page): #TestCase 3
    page.goto(BASE_URL)
    page.get_by_role("button", name="Any").click()
    page.get_by_role("option", name="10,000+").click()

    cell_1 = page.get_by_role("cell", name="64284")
    cell_1_value = int(cell_1.text_content().strip())
    assert cell_1_value >= 10000

    cell_2 = page.get_by_role("cell", name="14762")
    cell_2_value = int(cell_2.text_content().strip())
    assert cell_2_value >= 10000

    cell_3 = page.get_by_role("cell", name="16452")
    cell_3_value = int(cell_3.text_content().strip())
    assert cell_3_value >= 10000

    cell_4 = page.get_by_role("cell", name="10705")
    cell_4_value = int(cell_4.text_content().strip())
    assert cell_4_value >= 10000


def test_combined_filters_python_beginner_10000(page: Page): #TestCase 4
    page.goto(BASE_URL)
    # Select Language = Python
    page.locator("label").filter(has_text="Python").click()
    # Uncheck Intermediate and Advanced
    page.locator("label").filter(has_text="Intermediate").click()
    page.locator("label").filter(has_text="Advanced").click()
    # Set Min enrollments = 10,000+
    page.get_by_role("button", name="Any").click()
    page.get_by_role("option", name="10,000+").click()

    # Verify only Python Beginner courses with ≥ 10,000 enrollments are visible
    cell_language = page.get_by_role("cell", name="Python").first
    expect(cell_language).to_be_visible()
    cell_level = page.get_by_role("cell", name="Beginner").first
    expect(cell_level).to_be_visible()
    cell_enrollments = page.get_by_role("cell", name="10705")
    cell_enrollments_value = int(cell_enrollments.text_content().strip())
    assert cell_enrollments_value >= 10000


def test_no_results_state(page: Page): #TestCase 5
    page.goto(BASE_URL)
    # Select Language = Python
    page.locator("label").filter(has_text="Python").click()
    # Uncheck Beginner to leave only Advanced
    page.locator("label").filter(has_text="Beginner").click()
    # Verify "No matching courses." is shown
    assert page.get_by_text("No matching courses.", exact=True).first.is_visible()


def test_reset_button_visibility_and_behavior(page: Page): #TestCase 6
    page.goto(BASE_URL)
    page.locator("label").filter(has_text="Java").click()
    # Verify the Reset button becomes visible
    assert page.get_by_role("button", name="Reset").is_visible()
    page.get_by_role("button", name="Reset").click()
    # Verify Language = Any, all Levels checked, Min enrollments = Any
    expect(page.get_by_role("radio", name="Any")).to_be_checked()
    expect(page.locator("label").filter(has_text="Beginner")).to_be_checked()
    expect(page.locator("label").filter(has_text="Intermediate")).to_be_checked()
    expect(page.locator("label").filter(has_text="Advanced")).to_be_checked()
    expect(page.get_by_role("button", name="Any")).to_be_visible()
    # Verify the Reset button is hidden and all rows are visible
    expect(page.get_by_role("button", name="Reset")).not_to_be_visible()
    all_rows = page.get_by_role("row")
    expect(all_rows).to_have_count(10)


def test_sort_by_enrollments_ascending(page: Page):  #TestCase 7
    page.goto(BASE_URL)
    page.get_by_label("Sort by:").select_option("col_enroll") # Set Sort by = Enrollments
    # Wait briefly for the sort to apply
    page.wait_for_timeout(200)

    # Collect enrollment numbers from visible rows only and parse them
    rows = page.locator("table tbody tr:visible")
    count = rows.count()
    values = []
    for i in range(count):
        # Enrollments is in the 5th column (0-based index 4)
        text = rows.nth(i).locator("td").nth(4).inner_text().strip()
        # Remove commas and convert to int
        num = int(text.replace(",", ""))
        values.append(num)

    assert values == sorted(values), f"Enrollments NOT sorted ascending: {values}"


def test_sort_by_course_name_alphabetical(page: Page):  #TestCase 8
    page.goto(BASE_URL)
    page.get_by_label("Sort by:").select_option("col_course")  # Set Sort by = Course Name
    # Wait briefly for the sort to apply
    page.wait_for_timeout(200)

    rows = page.locator("table tbody tr:visible")
    count = rows.count()
    course_names = []
    for i in range(count):
        # Course name is in the 2nd column (0-based index 1)
        text = rows.nth(i).locator("td").nth(1).inner_text().strip()
        course_names.append(text)

    # Compare case-insensitively to avoid capitalization ordering issues
    assert course_names == sorted(course_names, key=str.lower), f"Course names NOT sorted A→Z: {course_names}"