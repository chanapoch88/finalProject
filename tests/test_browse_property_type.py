import pytest
import allure

from pages.browse_property_type import BrowsePropertyType

# To scroll to 'Browse by property type' section, print out the total number of categories and their names
@pytest.mark.browsePropertyType
@allure.suite("Browse by property type Suite")
def test_browse_property_type_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    tbpt1 = BrowsePropertyType(driver)
    tbpt1.dismiss_signin_popup()
    tbpt1.scroll_to_browse_by_property_type()
    tbpt1.list_browse_by_property_type()
    tbpt1.count_browse_by_property_type()

# To find a category listed in 'Browse by property type' section by text, click on it and verify correct page that opens
@pytest.mark.browsePropertyType
@allure.suite("Browse by property type Suite")
def test_browse_property_type_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    tbpt2 = BrowsePropertyType(driver)
    tbpt2.dismiss_signin_popup()
    tbpt2.scroll_to_browse_by_property_type()
    tbpt2.choose_category("Cottages")
    tbpt2.verify_results_title_contains("that appeal to you the most")

# To open a category in 'Browse by property type' section by text, scroll to 'Most booked' section, and
# find the name, location and rating of 1st listing
@pytest.mark.browsePropertyType
@allure.suite("Browse by property type Suite")
def test_browse_property_type_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    tbpt3 = BrowsePropertyType(driver)
    tbpt3.dismiss_signin_popup()
    tbpt3.scroll_to_browse_by_property_type()
    tbpt3.choose_category("Resorts")
    tbpt3.get_details_of_1st_most_booked_listing("Resorts")