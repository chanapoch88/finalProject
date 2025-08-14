import pytest
import allure

from pages.stays_search import StaysSearch

# To perform simple stay search via typed in full name of destination and verify results page
@pytest.mark.staysSearch
@allure.suite("Stays Search Suite")
def test_stays_choose_destination_byText_opens_page_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    s1 = StaysSearch(driver)
    s1.type_destination("Tel Aviv")
    s1.choose_start_date()
    s1.choose_end_date()
    s1.click_search_btn()
    watchword_byText, actual_title = s1.get_results_title_and_watchword()
    expected_partial_title = "properties found"
    assert watchword_byText in actual_title and expected_partial_title in actual_title, \
        f"'Expected to get both '{watchword_byText}' and '{expected_partial_title}' in the header but instead got '{actual_title}'"

# To perform simple stay search using autocompletion for name of destination and verify results page
@pytest.mark.staysSearch
@allure.suite("Stays Search Suite")
def test_stays_choose_random_destination_opens_page_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    s2 = StaysSearch(driver)
    s2.type_partial_destination("Am")
    s2.choose_random_start_date()
    s2.choose_random_end_date()
    s2.click_search_btn()
    s2.check_for_map_view()
    watchword_random, actual_title = s2.get_results_title_and_watchword()
    expected_partial_title = "properties found"
    assert watchword_random in actual_title and expected_partial_title in actual_title, \
        f"'Expected to get both '{watchword_random}' and '{expected_partial_title}' in the header but instead got '{actual_title}'"

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
    original_occupant_details = s3.check_occupancy()
    new_occupant_details = s3.change_occupants()
    assert new_occupant_details != original_occupant_details, \
        (f"Test failed. The occupancy details did not change as expected. "
         f"Default details: {original_occupant_details}, new occupancy details: {new_occupant_details}")