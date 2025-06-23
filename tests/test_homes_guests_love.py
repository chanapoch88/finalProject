import pytest
import allure

from pages.homes_guests_love import HomesGuestsLove

# To scroll to 'Homes Guests Love' section, print out the listing names and the total count
@pytest.mark.homesGuestsLove
@allure.suite("Homes Guests Love Suite")
def test_homes_guests_love_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    hgl1 = HomesGuestsLove(driver)
    hgl1.dismiss_signin_popup()
    hgl1.scroll_to_homes_guests_love()
    hgl1.list_homes_guests_love()
    hgl1.count_homes_guests_love()

# To find the name & rating of the highest rated listing in 'Homes Guests Love' section
@pytest.mark.homesGuestsLove
@allure.suite("Homes Guests Love Suite")
def test_homes_guests_love_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    hgl2 = HomesGuestsLove(driver)
    hgl2.dismiss_signin_popup()
    hgl2.scroll_to_homes_guests_love()
    hgl2.compare_ratings()

# To favorite the 1st listing in the 'Homes Guests Love' section
@pytest.mark.homesGuestsLove
@allure.suite("Homes Guests Love Suite")
def test_homes_guests_love_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    hgl3 = HomesGuestsLove(driver)
    hgl3.dismiss_signin_popup()
    hgl3.scroll_to_homes_guests_love()
    hgl3.add_1st_home_to_favorites()
    hgl3.verify_moved_to_favorites_page("My next trip")
    hgl3.verify_added_to_favorites("1 saved property")
