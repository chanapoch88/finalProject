import pytest
import allure

from pages.browse_property_type import BrowsePropertyType

# To scroll to 'Browse by property type' section, print out the total number of categories and their names
@pytest.mark.browsePropertyType
@allure.suite("Browse by property type Suite")
def test_browse_property_type_check_for_categories_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    tbpt1 = BrowsePropertyType(driver)
    tbpt1.dismiss_signin_popup()
    tbpt1.scroll_to_browse_by_property_type()
    tbpt1.list_browse_by_property_type()
    num_categories = tbpt1.count_browse_by_property_type()
    assert num_categories > 0, f"'The 'Browse by property type' section should contain at least 1 category but couldn't find any'"

# To find a category listed in 'Browse by property type' section by text, click on it and verify correct page that opens
@pytest.mark.browsePropertyType
@allure.suite("Browse by property type Suite")
def test_browse_property_choose_category_byText_opens_page_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    tbpt2 = BrowsePropertyType(driver)
    tbpt2.dismiss_signin_popup()
    tbpt2.scroll_to_browse_by_property_type()
    tbpt2.choose_category("Cottages")
    watchword, actual_title = tbpt2.get_category_page_title_and_watchword()
    expected_partial_title = "that appeal to you the most"
    assert watchword in actual_title and expected_partial_title in actual_title, \
        f"'Expected to get both '{watchword}' and '{expected_partial_title}' in the header but instead got '{actual_title}'"

# To open a category in 'Browse by property type' section by text, scroll to 'Most booked' section, and
# find the name, location and rating of 1st listing
@pytest.mark.browsePropertyType
@allure.suite("Browse by property type Suite")
def test_browse_property_type_find_most_booked_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    tbpt3 = BrowsePropertyType(driver)
    tbpt3.dismiss_signin_popup()
    tbpt3.scroll_to_browse_by_property_type()
    tbpt3.choose_category("Resorts")
    listing_details = tbpt3.get_details_of_1st_most_booked_listing("Resorts")

    if listing_details['category'] == "Hotels":
        watchword, actual_title = listing_details['title_details']
        expected_partial_title = "to luxury rooms and everything in between"
        assert watchword in actual_title and expected_partial_title in actual_title, \
            f"'Expected to get both '{watchword}' and '{expected_partial_title}' in the header but instead got '{actual_title}'"
    else:
        expected_category = listing_details['category']
        assert expected_category in listing_details['actual_page_header'], f"The page header '{expected_category}' was expected but instead got '{listing_details['actual_page_header']}'"

        assert listing_details['has_most_booked'], "'listing_details['category'] page' should have 'Most booked' section but doesn't."
        assert listing_details['most_booked_name'], "The 'Most booked' property does not display a name."
        assert listing_details['most_booked_place'], "The 'Most booked' property doesn't display a location."
        assert listing_details['most_booked_rating'], "No rating was found for the 'Most booked' property."