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
    plan1.test_category_with_fallback([
        {"category": "City", "destination": "Safed"},
        {"category": "Beach Relaxation", "destination": "Haifa"}
    ])
    plan1.verify_results_title_contains("properties found")

# In specific destination page, sort properties by highest to lowest and print out their ratings in that order
@pytest.mark.tripPlanner
@allure.suite("Trip Planner Suite")
def test_trip_plan2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan2 = TripPlanner(driver)
    plan2.dismiss_signin_popup()
    plan2.scroll_to_trip_planner()
    plan2.test_category_with_fallback([
        {"category": "Outdoors", "destination": "Ein Bokek"},
        {"category": "Night Entertainments", "destination": "Rechovot"}
    ])
    plan2.printout_num_properties_found()

# In specific destination page, sort properties by highest to lowest and verify that sort type changed
@pytest.mark.tripPlanner
@allure.suite("Trip Planner Suite")
def test_trip_plan3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan3 = TripPlanner(driver)
    plan3.dismiss_signin_popup()
    plan3.scroll_to_trip_planner()
    plan3.test_category_with_fallback([
        {"category": "City", "destination": "Caesarea"},
        {"category": "Festival Attendance", "destination": "Ramat Gan"}
    ])
    plan3.choose_property_sort_type("Property rating (low to high)")
    plan3.verify_sort_type_changed("Sort by: Property rating (low to high)")

# In specific destination page, sort properties by highest to lowest and print out their ratings in that order
@pytest.mark.tripPlanner
@allure.suite("Trip Planner Suite")
def test_trip_plan4(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan4 = TripPlanner(driver)
    plan4.dismiss_signin_popup()
    plan4.scroll_to_trip_planner()
    plan4.test_category_with_fallback([
        {"category": "City", "destination": "Caesarea"},
        {"category": "Festival Attendance", "destination": "Ramat Gan"}
    ])
    plan4.choose_property_sort_type("Property rating (high to low)")
    plan4.verify_sort_type_changed("Sort by: Property rating (high to low)")
    plan4.printout_10highest_results()

# In specific destination page, sort properties by highest to lowest and print out their ratings in that order
@pytest.mark.tripPlanner
@allure.suite("Trip Planner Suite")
def test_trip_plan5(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan5 = TripPlanner(driver)
    plan5.dismiss_signin_popup()
    plan5.scroll_to_trip_planner()
    plan5.test_category_with_fallback([
        {"category": "City", "destination": "Jerusalem"},
        {"category": "Beach Relaxation", "destination": "Bat Yam"}
    ])
    plan5.filter_by_highest_review_score()
    plan5.verify_highest_score_filter_btn_appears()
    plan5.verify_all_listed_ratings_over_9()