import pytest
import allure

from pages.trip_planner import TripPlanner

# To verify specific destination page opens when press click on destination tile in 'Quick and easy trip planner' section
@pytest.mark.tripPlanner
@allure.suite("Trip Planner Suite")
def test_trip_plan_destination_tile_opens_destination_page_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan1 = TripPlanner(driver)
    plan1.dismiss_signin_popup()
    plan1.scroll_to_trip_planner()
    plan1.test_category_with_fallback([
        {"category": "City", "destination": "Safed"},
        {"category": "Beach Vacations", "destination": "Haifa"}
    ])
    watchword, actual_page_title = plan1.get_results_title_and_watchword()
    expected_partial_title = "properties found"
    assert watchword in actual_page_title and expected_partial_title in actual_page_title, \
        f"'Expected to get both '{watchword}' and '{expected_partial_title}' in the header but instead got '{actual_page_title}'"

# In specific destination page, find number of properties listed, verify that count is > 0 and
# location and property number match page header details
@pytest.mark.tripPlanner
@allure.suite("Trip Planner Suite")
def test_trip_plan_destination_results_matches_destination_page_header_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan2 = TripPlanner(driver)
    plan2.dismiss_signin_popup()
    plan2.scroll_to_trip_planner()
    plan2.test_category_with_fallback([
        {"category": "Outdoors", "destination": "Ein Bokek"},
        {"category": "City Breaks", "destination": "Rechovot"}
    ])
    selected_destination = plan2.chosen_destination_name
    property_location, num_properties = plan2.get_num_properties_at_location()
    trip_planner_results_count = plan2.get_num_listings_on_results_page(selected_destination)

    assert int(num_properties) > 0, "Should have found at least 1 property"
    assert int(num_properties) == trip_planner_results_count, \
        (f"Expected the tile count on the trip planner results page for '{property_location}' "
         f"to equal '{num_properties}' listed in the page header but got '{trip_planner_results_count}' instead")

# In specific destination page, sort properties by highest to lowest and verify that sort type changed
@pytest.mark.tripPlanner
@allure.suite("Trip Planner Suite")
def test_sort_trip_plan_destination_results_high_to_low_and_verify_sort_type_changed_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan3 = TripPlanner(driver)
    plan3.dismiss_signin_popup()
    plan3.scroll_to_trip_planner()
    plan3.test_category_with_fallback([
        {"category": "City", "destination": "Haifa"},
        {"category": "Festivals", "destination": "Beer Sheva"}
    ])
    plan3.choose_property_sort_type("Property rating (low to high)")
    expected_sort_type = "Sort by: Property rating (low to high)"
    tries, final_sort_type_name = plan3.has_sort_type_changed("Property rating (low to high)")

    assert final_sort_type_name == expected_sort_type, \
        (f"The sort type did not update to match {expected_sort_type}. "
         f"After checking {tries} times, the sort type is: {final_sort_type_name}")

# In destination page, compare properties sorted by lowest to highest with the same properties
# sorted by highest to lowest and verify that properties listed changes between the two sort types
@pytest.mark.tripPlanner
@allure.suite("Trip Planner Suite")
def test_compare_2_sorted_property_results_and_verify_listings_change_4(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan4 = TripPlanner(driver)
    plan4.dismiss_signin_popup()
    plan4.scroll_to_trip_planner()
    plan4.test_category_with_fallback([
        {"category": "City", "destination": "Tiberias"},
        {"category": "Festivals", "destination": "Netanya"}
    ])
    plan4.choose_property_sort_type("Property rating (high to low)")
    plan4.has_sort_type_changed("Property rating (low to high)")
    low_to_high_top10_sorting_results = plan4.collect_limited_property_results_details(10)

    print("The top 10 properties and their corresponding ratings when sorted high to low are:")
    for index, result in enumerate(low_to_high_top10_sorting_results):
        print(f"#{index + 1}: '{result[0]}' with a rating of {result[1]}", sep='\n')

    plan4.choose_property_sort_type("Property rating (high to low)")
    plan4.has_sort_type_changed("Property rating (high to low)")
    high_to_low_top10_sorting_results = plan4.collect_limited_property_results_details(10)

    print("The top 10 properties and their corresponding ratings when sorted high to low are:")
    for index, result in enumerate(high_to_low_top10_sorting_results):
        print(f"#{index + 1}: '{result[0]}' with a rating of {result[1]}", sep='\n')

    assert high_to_low_top10_sorting_results != low_to_high_top10_sorting_results, \
        f"After changing the sort criteria, the order of the properties should be sorted differently but weren't."

# In specific destination page, sort properties by highest to lowest and print out their ratings in that order
@pytest.mark.tripPlanner
@allure.suite("Trip Planner Suite")
def test_verify_highest_score_filter_shows_only_properties_with_score_9_or_more_trip_plan_5(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    plan5 = TripPlanner(driver)
    plan5.dismiss_signin_popup()
    plan5.scroll_to_trip_planner()
    plan5.test_category_with_fallback([
        {"category": "City", "destination": "Jerusalem"},
        {"category": "Beach Vacations", "destination": "Bat Yam"}
    ])
    plan5.filter_by_highest_review_score()
    highest_score_filter_btn_displayed = plan5.does_highest_score_filter_btn_appear()
    assert highest_score_filter_btn_displayed, f"Could not find the highest review score filter button displayed within the set time"

    properties_with_lower_score_details = plan5.get_all_listed_ratings_under_9()
    assert properties_with_lower_score_details == False, f"Expected all filtered properties to score '9' or more but these properties didn't: {properties_with_lower_score_details}"
