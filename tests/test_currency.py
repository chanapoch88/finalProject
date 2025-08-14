import pytest
import allure

from pages.currency import Currency

# To verify that the currency window opens after press on currency button
@pytest.mark.currency
@allure.suite("Currency Suite")
def test_currency_button_opens_window_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    curr1 = Currency(driver)
    curr1.open_currency_window()
    actual_window_title = curr1.get_currency_window_title()
    expected_window_title = "Select your currency"
    assert expected_window_title == actual_window_title, f"The window header '{expected_window_title}' was expected but instead got '{actual_window_title}'"

# To verify that the main page opens after the currency window is closed
@pytest.mark.currency
@allure.suite("Currency Suite")
def test_main_page_reopens_after_currency_window_closed_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    curr2 = Currency(driver)
    curr2.open_currency_window()
    actual_currency_window_title = curr2.get_currency_window_title()
    expected_currency_window_title = "Select your currency"
    assert expected_currency_window_title == actual_currency_window_title, f"The window header '{expected_currency_window_title}' was expected but instead got '{actual_currency_window_title}'"
    curr2.close_currency_window()
    expected_main_page_title = "Find your next stay"
    actual_page_title = curr2.get_main_page_title()
    assert expected_main_page_title == actual_page_title, f"Expected to get the main page header '{expected_main_page_title}' but got '{actual_page_title} instead.'"

# To change to US currency type within 'Selected for you' section and verify that change was made
@pytest.mark.currency
@allure.suite("Currency Suite")
def test_change_selected_currency_and_verify_change_made_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    curr3 = Currency(driver)
    curr3.open_currency_window()
    curr3.select_us_currency_type()
    expected_currency_type = "USD"
    current_currency_type = curr3.get_new_currency_value()
    assert current_currency_type == expected_currency_type, f"Test failed. Currency type did not change to '{expected_currency_type}', got '{current_currency_type}' instead."

# To change currency type within 'All currencies' section according to text and verify that change was made
@pytest.mark.currency
@allure.suite("Currency Suite")
def test_change_currency_byText_and_verify_change_made_4(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    curr3 = Currency(driver)
    curr3.open_currency_window()
    curr3.select_currency_type_by_text("Chinese Yuan")
    expected_currency_type = "CNY"
    actual_currency_type = curr4.get_new_currency_value()
    assert actual_currency_type == expected_currency_type, f"Currency type failed to change to '{expected_currency_type}', displayed '{actual_currency_type}' instead."
