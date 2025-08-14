import pytest
import allure

from pages.trending_destinations import TrendingDestinations

# To print out the list of destinations in 'Trending destinations among travelers from Israel' section and
# to verify that there are 5 destination tiles
@pytest.mark.trendingDestinations
@allure.suite("Trending Destinations Suite")
def test_trending_destinations_tile_details_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan1 = TrendingDestinations(driver)
    plan1.dismiss_signin_popup()
    plan1.scroll_to_trending_destinations()
    all_trending_destinations_list = plan1.get_trending_destinations_tile_details()
    number_trending_destinations_tiles = len(all_trending_destinations_list)

    assert number_trending_destinations_tiles == 5, f"Expected to get a total of 5 trending destination tiles but got {number_trending_destinations_tiles} instead"