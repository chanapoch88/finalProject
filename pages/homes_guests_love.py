import time

from selenium.webdriver.common.by import By

from pages.base_page import Base


class HomesGuestsLove(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.category_name = "Homes Guests Love"

    homes_guests_love_section = (By.CLASS_NAME, 'b3646cd8c2')
    homes_guests_love_group = (By.XPATH, "//ul[@aria-label='Homes guests love']")
    homes_guests_love_listing_names = (By.XPATH, "//ul[@aria-label='Homes guests love']//div[contains(@class, 'ecb8d66605 cf0e25a46d')]/h3")
    homes_guests_love_rating_info = (By.XPATH, "//ul[@aria-label='Homes guests love']//div[@data-testid='webcore-carousel-review']")
    homes_guests_love_ratings = (By.XPATH, "//ul[@aria-label='Homes guests love']//div[@data-testid='webcore-carousel-review']//div[@class='bc946a29db'][1]")
    first_home_guests_love_heart = (By.XPATH, "//ul[@aria-label='Homes guests love']/li[@class='ee4cb4021c c3bfe61347'][1]//button")
    my_next_trip_link = (By.XPATH, "//div[@data-testid='wishlist-popover-content']//a")
    my_next_trip_header = (By.TAG_NAME, "h1")
    favorites_property_text = (By.XPATH, "//div[contains(@class, 'd8df6227ee')]//div[@class='b99b6ef58f']")


    def scroll_to_homes_guests_love(self):
        self.scroll_to_element(self.homes_guests_love_group)
        self.wait_for_element_visibility(self.homes_guests_love_group)

    def list_homes_guests_love(self):
        print(f"The names listed of the homes that guests love are:")
        home_names = self.driver.find_elements(*self.homes_guests_love_listing_names)
        self.print_list_elements(home_names)

    def count_homes_guests_love(self):
        home_names = self.driver.find_elements(*self.homes_guests_love_listing_names)
        self.count_elements(home_names, self.category_name)

    def get_home_ratings(self):
        property_ratings_list = []
        listed_property_ratings = self.wait_for_element(self.homes_guests_love_ratings)
        for r in listed_property_ratings:
            property_ratings_list.append(r)
        return property_ratings_list

    def compare_ratings(self):
        name_elements = self.driver.find_elements(*self.homes_guests_love_listing_names)
        rating_elements = self.driver.find_elements(*self.homes_guests_love_ratings)

        homes_guests_love_names_list = self.create_list_of_elements(name_elements)
        homes_guests_love_ratings_list = self.create_list_of_elements(rating_elements)
        self.compare_lists_highest_value(homes_guests_love_names_list, homes_guests_love_ratings_list, "rating")

    def add_1st_home_to_favorites(self):
        self.wait_and_click(self.first_home_guests_love_heart)

    def verify_moved_to_favorites_page(self, expected_header):
        self.wait_and_click(self.my_next_trip_link)
        self.move_to_new_tab()
        time.sleep(2)
        self.check_window_state(self.my_next_trip_header, expected_header)

    def verify_added_to_favorites(self, partial_expected_header):
        self.verify_page_header(self.favorites_property_text, partial_expected_header)