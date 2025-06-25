import pytest
import allure

from pages.main_nav import MainNav

# To verify flight page opens when press Flights main nav button
@pytest.mark.mainNav
@allure.suite("Main Nav Suite")
def test_main_nav1_flights(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    nav1 = MainNav(driver)
    nav1.open_navigated_to_window("Flights")
    nav1.verify_opened_correct_page("Flights", "Search hundreds of flight sites at once.")

def test_main_nav2_cars(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    nav1 = MainNav(driver)
    nav1.open_navigated_to_window("Car rentals")
    nav1.verify_opened_correct_page("Car rentals","Car rentals for any kind of trip")

def test_main_nav3_attractions(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    nav1 = MainNav(driver)
    nav1.open_navigated_to_window("Attractions")
    nav1.verify_opened_correct_page("Attractions","Attractions, activities, and experiences")

def test_main_nav4_taxis(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    nav1 = MainNav(driver)
    nav1.open_navigated_to_window("Airport taxis")
    nav1.verify_opened_correct_page("Airport taxis","Find the right ride for your trip")