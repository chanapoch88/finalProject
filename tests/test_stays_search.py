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

# To perform simple stay search using autocompletion for name of destination
@pytest.mark.staysSearch
@allure.suite("Stays Search Suite")
def test_stays_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    s2 = StaysSearch(driver)
    s2.type_partial_destination("Am")
    s2.choose_random_start_date()
    s2.choose_random_end_date()
    s2.click_search_btn()
    s2.check_for_map_view()
    s2.verify_results_title_contains("properties found")

# To verify change made in occupancy
@pytest.mark.staysSearch
@allure.suite("Stays Search Suite")
def test_stays_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    s3 = StaysSearch(driver)
    s3.type_destination("Atlanta")
    s3.choose_start_date()
    s3.choose_end_date()
    s3.check_occupancy()
    s3.change_occupants()
    s3.verify_occupancy_change()