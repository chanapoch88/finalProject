import pytest
import allure

from pages.trip_planner import TripPlanner

# To verify specific destination page opens when press click on destination tile in 'Quick and easy trip planner' section
@pytest.mark.tripPlanner
@allure.suite("Trip Planner Suite")
def test_trip_plan1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan1 = TripPlanner(driver)
    plan1.dismiss_signin_popup()
    plan1.scroll_to_trip_planner()
    plan1.choose_trip_plan_category("City")
    plan1.choose_trip_destination("Safed")
    plan1.verify_results_title_contains("properties found")