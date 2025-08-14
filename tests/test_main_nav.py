import pytest
import allure

from pages.main_nav import MainNav

# To verify flight page opens when press Flights main nav button
@pytest.mark.mainNav
@allure.suite("Main Nav Suite")
def test_flights_main_nav_btn_opens_window_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    nav1 = MainNav(driver)
    nav1.open_navigated_to_window("Flights")
    expected_flights_nav_header = "Search hundreds of flight sites at once."
    actual_nav_header = nav1.get_opened_nav_page_header_from_nav_name("Flights")
    assert actual_nav_header == expected_flights_nav_header, f"The window header '{expected_flights_nav_header}' was expected but instead got '{actual_nav_header}'"

def test_cars_main_nav_btn_opens_window_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    nav2 = MainNav(driver)
    nav2.open_navigated_to_window("Car rentals")
    expected_cars_nav_header = "Car rentals for any kind of trip"
    actual_nav_header = nav2.get_opened_nav_page_header_from_nav_name("Car rentals")
    assert actual_nav_header == expected_cars_nav_header, f"The window header '{expected_cars_nav_header}' was expected but instead got '{actual_nav_header}'"

def test_attractions_main_nav_btn_opens_window_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    nav3 = MainNav(driver)
    nav3.open_navigated_to_window("Attractions")
    expected_attractions_nav_header = "Attractions, activities, and experiences"
    actual_nav_header = nav3.get_opened_nav_page_header_from_nav_name("Attractions")
    assert actual_nav_header == expected_attractions_nav_header, f"The window header '{expected_attractions_nav_header}' was expected but instead got '{actual_nav_header}'"

def test_taxis_main_nav_btn_opens_window_4(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    nav4 = MainNav(driver)
    nav4.open_navigated_to_window("Airport taxis")
    expected_taxis_nav_header = "Find the right ride for your trip"
    actual_nav_header = nav4.get_opened_nav_page_header_from_nav_name("Airport taxis")
    assert actual_nav_header == expected_taxis_nav_header, f"The window header '{expected_taxis_nav_header}' was expected but instead got '{actual_nav_header}'"
