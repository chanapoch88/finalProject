import pytest
import allure

from pages.list_property import ListProperty

# To verify that pressing 'List your property' button opens Join listings page
@pytest.mark.list_property
# @allure.suite("List Property Suite")
def test_list_property_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    list_prop1 = ListProperty(driver)
    list_prop1.open_list_property_window()
    list_prop1.verify_join_listings_page("Join", "other listings already on Booking.com")