import pytest
import allure

from pages.stays_search import StaysSearch

# To perform simple stay search via typed in full name of destination
@pytest.mark.staysSearch
@allure.suite("Stays Search Suite")
def test_stays_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    s1 = StaysSearch(driver)
    s1.type_destination("Tel Aviv")
    s1.choose_start_date()
    s1.choose_end_date()
    s1.click_search_btn()
    s1.verify_results_title_contains("properties found")
