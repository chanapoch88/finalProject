from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import Base


class MainNav(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.nav_name_to_btn_locator = {
            "Stays": self.stays_nav_btn,
            "Flights": self.flights_nav_btn,
            "Car rentals": self.car_rental_nav_btn,
            "Attractions": self.attractions_nav_btn,
            "Airport taxis": self.airport_taxis_nav_btn
        }
        self.nav_name_to_header_locator = {
            # "Stays": self.stays_nav_btn,
            "Flights": self.search_flights_page_header,
            "Car rentals": self.search_cars_page_header,
            "Attractions": self.search_attractions_page_header,
            "Airport taxis": self.search_taxis_page_header
        }

    stays_nav_btn = (By.ID, "accommodations")
    flights_nav_btn = (By.ID, "flights")
    car_rental_nav_btn = (By.ID, "cars")
    attractions_nav_btn = (By.ID, "attractions")
    airport_taxis_nav_btn = (By.ID, "airport_taxis")
    search_flights_page_header = (By.XPATH, "//span[@class='oaFt-title']")
    search_cars_page_header = (By.TAG_NAME, "h1")
    search_attractions_page_header = (By.TAG_NAME, "h1")
    search_taxis_page_header = (By.TAG_NAME, "h1")


    def choose_nav_btn(self, nav_name):
        print("Trying to match the entered title to its navigation button...")
        if nav_name.capitalize() not in self.nav_name_to_btn_locator:
            raise ValueError(f"'{nav_name}' navigation button is not defined.")
        return self.nav_name_to_btn_locator[nav_name.capitalize()]

    def open_navigated_to_window(self, nav_name):
        print("Clicking on the nav button...")
        self.dismiss_signin_popup()
        chosen_nav_locator = self.choose_nav_btn(nav_name)
        self.wait_and_click(chosen_nav_locator)
        return chosen_nav_locator

    def get_opened_nav_page_header_from_nav_name(self, nav_name):
        header_locator = self.nav_name_to_header_locator[nav_name]
        self.wait_for_element_visibility(header_locator)
        nav_page_header = self.get_page_header_text(header_locator)
        return nav_page_header