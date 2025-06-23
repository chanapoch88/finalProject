import pytest
import allure

from pages.currency import Currency

# To verify that the currency window opens after press on currency button
@pytest.mark.currency
@allure.suite("Currency Suite")
def test_currency_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    curr1 = Currency(driver)
    curr1.open_currency_window()
    curr1.check_for_currency_window("Select your currency")

# To verify that the main page opens after the currency window is closed
@pytest.mark.currency
@allure.suite("Currency Suite")
def test_currency_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    curr2 = Currency(driver)
    curr2.open_currency_window()
    curr2.check_for_currency_window("Select your currency")
    curr2.close_currency_window()
    curr2.verify_main_page_open("Find your next stay")

# To change to US currency type within 'Selected for you' section and verify that change was made
@pytest.mark.currency
@allure.suite("Currency Suite")
def test_currency_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    curr3 = Currency(driver)
    curr3.open_currency_window()
    curr3.select_us_currency_type()
    curr3.verify_currency_value_changed("USD")

# To change currency type within 'All currencies' section according to text and verify that change was made
@pytest.mark.currency
@allure.suite("Currency Suite")
def test_currency_4(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    curr3 = Currency(driver)
    curr3.open_currency_window()
    curr3.select_currency_type_by_text("Chinese Yuan")
    curr3.verify_currency_value_changed("CNY")