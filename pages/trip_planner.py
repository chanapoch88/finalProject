import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import Base


class TripPlanner(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.chosen_category_name = None
        self.chosen_destination_name = None

    trip_planner_section_title = (By.XPATH, "//div[@data-qmab-component-id='44']//h2")
    trip_planner_group = (By.XPATH, "//ul[@aria-label='Quick and easy trip planner']")
    trip_planner_category_buttons = (By.XPATH, "//nav[@data-testid='webcore-filter-carousel-tabs']//li")
    trip_planner_destination_next_btn = (By.XPATH, "//div[@data-qmab-component-id='44']//button[@aria-label='Next']/span")
    trip_planner_destination_tiles = (By.XPATH, "//ul[@aria-label='Quick and easy trip planner']/li")
    trip_planner_destination_page_header = (By.TAG_NAME, "h1")

    def scroll_to_trip_planner(self):
        self.scroll_to_element(self.trip_planner_section_title)
        self.wait_for_element_visibility(self.trip_planner_section_title)

    def choose_trip_plan_category(self, trip_category):
        self.wait.until(EC.presence_of_all_elements_located(self.trip_planner_category_buttons))
        all_trip_plan_categories = self.driver.find_elements(*self.trip_planner_category_buttons)

        for category in all_trip_plan_categories:
            category_name = category.find_element(By.XPATH, ".//button//div/span").text

            if category_name == trip_category.capitalize():
                print(f"The chosen trip category is: {category_name}")
                category_link = category.find_element(By.XPATH,f".//button[.//span[contains(text(), '{category_name}')]]")
                time.sleep(1)
                try:
                    self.wait.until(EC.element_to_be_clickable(category_link)).click()
                except Exception as e:
                    print(f"Couldn't click due to {e}, so now trying with JavaScript click...")
                    self.driver.execute_script("arguments[0].click();", category_link)

                self.chosen_category_name = category_name.capitalize()
                return
        raise ValueError(f"Could not find the destination '{trip_category}'")


    def choose_trip_destination(self, destination):
        self.wait.until(EC.presence_of_all_elements_located(self.trip_planner_destination_tiles))

        all_trip_destinations = self.driver.find_elements(*self.trip_planner_destination_tiles)

        for trip in all_trip_destinations:
            try:
                self.scroll_to_element(trip)
                time.sleep(1)
                destination_name = trip.find_element(By.TAG_NAME, "h3").text

                if destination_name == destination.capitalize():
                    print(f"The chosen destination is: {destination_name.capitalize()}")
                    destination_link = trip.find_element(By.TAG_NAME, "a")

                    try:
                        self.wait.until(EC.element_to_be_clickable(destination_link)).click()
                    except Exception as e:
                        print(f"Couldn't click {destination.capitalize()} due to {e}")
                        print(f"\nScrolling to bring tile into view and trying click again...")

                        try:
                            self.scroll_to_element(destination_link)
                            time.sleep(1)
                            destination_link.click()

                        except Exception as e:
                            print(f"Clicking {destination.capitalize()} failed: {e}")
                            print(f"\nWill try JavaScript click...")
                            self.driver.execute_script("arguments[0].click();", destination_link)

                    self.chosen_destination_name = destination_name.capitalize()
                    return
            except Exception as e:
                print(f"Issue found with tile: {e}")
                continue

        raise ValueError(f"The destination '{destination}' wasn't found among the listed destinations")

    def verify_results_title_contains(self, partial_expected_header):
        watchword = self.chosen_destination_name
        self.move_to_new_tab()
        self.click_to_release_focus()
        self.verify_partial_title(self.trip_planner_destination_page_header, watchword, partial_expected_header)