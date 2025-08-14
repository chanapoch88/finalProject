from selenium.webdriver.common.by import By

from pages.base_page import Base


class TrendingDestinations(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.chosen_category_name = None
        self.chosen_destination_name = None
        self.original_sort_type_name = None

    trending_destinations_section_title = (By.XPATH, "//div[@data-testid='destination-postcards-title']//h2")
    trending_destinations_names_top_row = (By.XPATH, "//div[@data-testid='destination-postcards-firstrow']//a")
    trending_destinations_names_2nd_row = (By.XPATH, "//div[@data-testid='destination-postcards-secondrow']//a")

    def scroll_to_trending_destinations(self):
        self.scroll_to_element(self.trending_destinations_section_title)
        self.wait_for_element_visibility(self.trending_destinations_section_title)

    def printout_trending_destinations(self):
        first_row_trending_destinations_results = self.driver.find_elements(*self.trending_destinations_names_top_row)
        second_row_trending_destinations_results = self.driver.find_elements(*self.trending_destinations_names_2nd_row)

        first_row_destinations_names = self.create_list_of_elements(first_row_trending_destinations_results)
        all_trending_destinations_list = [el1.text for el1 in first_row_destinations_names]

        second_row_destinations_names = self.create_list_of_elements(second_row_trending_destinations_results)
        second_row_destinations_names_text = [el2.text for el2 in second_row_destinations_names]

        all_trending_destinations_list.extend(second_row_destinations_names_text)

        print("The top trending destinations are:")
        for i, d in enumerate(all_trending_destinations_list):
            if i < len(all_trending_destinations_list) - 1:
                print(d, end=", ")
            else:
                print(f"and {d}", end="")

        return all_trending_destinations_list