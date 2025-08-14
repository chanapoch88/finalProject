import pytest
import allure

from pages.homes_guests_love import HomesGuestsLove

# To scroll to 'Homes Guests Love' section, print out listing names and total count and verify count
@pytest.mark.homesGuestsLove
@allure.suite("Homes Guests Love Suite")
def test_homes_guests_love_verify_has_listings_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    hgl1 = HomesGuestsLove(driver)
    hgl1.dismiss_signin_popup()
    hgl1.scroll_to_homes_guests_love()
    hgl1.list_homes_guests_love()
    num_homes = hgl1.count_homes_guests_love()
    assert num_homes > 0, f"'The 'Homes Guests Love' section should contain at least 1 home listed but couldn't find any'"

# To find and verify the name & rating of the highest rated listing in 'Homes Guests Love' section
@pytest.mark.homesGuestsLove
@allure.suite("Homes Guests Love Suite")
def test_homes_guests_love_find_highest_rated_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    hgl2 = HomesGuestsLove(driver)
    hgl2.dismiss_signin_popup()
    hgl2.scroll_to_homes_guests_love()
    highest_rated_name, highest_rating = hgl2.compare_ratings()
    assert highest_rated_name, "No name was returned for the highest rated 'Homes Guests Love'"
    assert isinstance(highest_rating, float), f"The rating should be a float but instead the {type(highest_rating)} was given"
    assert highest_rating >= 8.0, f"Expected that the highest rating would be >= 8.0 but instead got {highest_rating} for {highest_rated_name}"

# To favorite the 1st listing in the 'Homes Guests Love' section and verify details
@pytest.mark.homesGuestsLove
@allure.suite("Homes Guests Love Suite")
def test_homes_guests_love_add_favorite_and_verify_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    hgl3 = HomesGuestsLove(driver)
    hgl3.dismiss_signin_popup()
    hgl3.scroll_to_homes_guests_love()
    hgl3.add_1st_home_to_favorites()
    hgl3.click_on_next_trip_link()
    expected_page_title = "My next trip"
    actual_page_title = hgl3.get_favorites_page_header_text()
    assert actual_page_title == expected_page_title, f"Page title should have been '{expected_page_title}' but it was '{actual_page_title}' instead."
    expected_favorites_text = "1 saved property"
    actual_favorites_text = hgl3.get_text_added_to_favorites_page()
    assert actual_favorites_text, f"No Favorites text was found."
    assert actual_favorites_text == expected_favorites_text, f"The favorites text '{expected_favorites_text}' was expected but instead got '{actual_favorites_text}'."
