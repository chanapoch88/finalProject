import pytest
import allure

from pages.list_property import ListProperty

# To verify that pressing 'List your property' button opens Join listings page
@pytest.mark.list_property
@allure.suite("List Property Suite")
def test_list_property_button_opens_window_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    list_prop1 = ListProperty(driver)
    list_prop1.open_list_property_window()
    watchword = "Join"
    expected_partial_title = "other listings already on Booking.com"
    actual_title = list_prop1.get_join_listings_page_header()
    assert watchword in actual_title and expected_partial_title in actual_title, \
        f"'Expected to get both '{watchword}' and '{expected_partial_title}' in the header but instead got '{actual_title}'"
