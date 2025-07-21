import pytest
import allure

from pages.trending_destinations import TrendingDestinations

# To print out the list of destinations in 'Trending destinations among travelers from Israel' section
@pytest.mark.trendingDestinations
@allure.suite("Trending Destinations Suite")
def test_trip_plan1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan1 = TrendingDestinations(driver)
    plan1.dismiss_signin_popup()
    plan1.scroll_to_trending_destinations()
    plan1.printout_trending_destinations()