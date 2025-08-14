import re
import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import Base


class TripPlanner(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.chosen_category_name = None
        self.chosen_destination_name = None
        self.original_sort_type_name = None

    trip_planner_section_title = (By.XPATH, "//div[@data-qmab-component-id='44']//h2")
    trip_planner_group = (By.XPATH, "//ul[@aria-label='Quick and easy trip planner']")
    trip_planner_category_buttons = (By.XPATH, "//nav[@data-testid='webcore-filter-carousel-tabs']//li")
    trip_planner_destination_tiles = (By.XPATH, "//ul[@aria-label='Quick and easy trip planner']/li")
    trip_planner_destination_page_header = (By.TAG_NAME, "h1")
    trip_planner_destination_tiles = (By.XPATH, "//ul[@aria-label='Quick and easy trip planner']/li")
    trip_planner_destination_page_header = (By.TAG_NAME, "h1")
    searchbox_whole_element = (By.XPATH, "//div[@data-testid='searchbox-layout-wide']")
    calendar_date_searchbox = (By.XPATH, "//button[@data-testid='searchbox-dates-container']")
    calendar_date_picker_open = (By.XPATH, "//div[@role='tabpanel']")
    trip_planner_sort_btn = (By.XPATH, "//button[@data-testid='sorters-dropdown-trigger']")
    trip_planner_sort_type = (By.XPATH, "//button[@data-testid='sorters-dropdown-trigger']//span[contains(text(), 'Sort by')]")
    trip_planner_sort_choice_list = (By.XPATH, "//div[@data-testid='sorters-dropdown']/ul")
    trip_planner_sort_choice_list_elements = (By.XPATH, "//div[@data-testid='sorters-dropdown']/ul/li")
    all_trip_planner_results_property_tiles = (By.XPATH, "//div[@data-testid='property-card']")
    all_trip_planner_results_names = (By.XPATH, "//div[@data-testid='property-card']//a[@data-testid='title-link']/div[@data-testid='title']")
    all_trip_planner_results_ratings = (By.XPATH, "//div[@data-testid='property-card']//div[@data-testid='review-score']/div[@class='bc946a29db']")
    review_score_filter_section = (By.XPATH, "//div[@data-filters-group='review_score']")
    review_score_filter_9plus_checkbox = (By.XPATH, "//div[@data-filters-item='review_score:review_score=90']//span[@class='c850687b9b']")
    review_score_filter_9plus_section_label = (By.XPATH, "//button[@id=':Ralmqcnr5:']//span[contains(text(), 'Review score')]")
    highest_review_score_filter_button = (By.XPATH, "//button[@data-testid='filter:review_score=90']")

    def scroll_to_trip_planner(self):
        print("Scrolling to Trip Planner section...")
        try:
            self.scroll_to_element(self.trip_planner_section_title)
            self.wait_for_element_visibility(self.trip_planner_section_title)
        except TimeoutException:
            raise AssertionError("Trip Planner section has not displayed")

    def choose_trip_plan_category(self, trip_category):
        self.wait.until(EC.presence_of_all_elements_located(self.trip_planner_category_buttons))
        all_trip_plan_categories = self.driver.find_elements(*self.trip_planner_category_buttons)
        displayed_categories = [c for c in all_trip_plan_categories if c.is_displayed()]

        for category in displayed_categories:
            category_name = category.find_element(By.XPATH, ".//button//div/span")
            self.wait.until(EC.visibility_of(category_name))
            category_name_text = category_name.text

            if category_name_text == trip_category.title():
                print(f"The chosen trip category is: {category_name_text}")
                category_link = category.find_element(By.XPATH, f".//button[.//span[contains(text(), '{category_name_text}')]]")
                time.sleep(1)
                try:
                    self.wait_and_click(category_link)
                except Exception as e:
                    print(f"Couldn't click due to {e}, so now trying JavaScript click...")
                    self.driver.execute_script("arguments[0].click();", category_link)

                self.chosen_category_name = category_name_text.title()
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

                if destination_name == destination.title():
                    print(f"The chosen destination is: {destination_name.title()}")
                    destination_link = trip.find_element(By.TAG_NAME, "a")

                    try:
                        self.wait.until(EC.element_to_be_clickable(destination_link)).click()
                    except Exception as e:
                        print(f"Couldn't click {destination.title()} due to {e}")
                        print(f"\nScrolling to bring tile into view and trying click again...")

                        try:
                            self.scroll_to_element(destination_link)
                            time.sleep(1)
                            destination_link.click()

                        except Exception as e:
                            print(f"Clicking {destination.title()} failed: {e}")
                            print(f"\nWill try JavaScript click...")
                            self.driver.execute_script("arguments[0].click();", destination_link)

                    self.chosen_destination_name = destination_name.title()
                    return
            except Exception as e:
                print(f"Issue found with tile: {e}")
                continue

        raise ValueError(f"The destination '{destination}' wasn't found among the listed destinations")

    def move_to_new_tab_and_free_focus(self):
        self.move_to_new_tab()
        self.click_to_release_focus()

    def get_results_title_and_watchword(self):
        watchword = self.chosen_destination_name
        self.move_to_new_tab_and_free_focus()
        actual_page_header = self.get_element_text(self.trip_planner_destination_page_header)
        print(f"watchword: {watchword}, actual_header: {actual_page_header}")
        return watchword, actual_page_header

    def get_num_properties_at_location(self):
        self.move_to_new_tab_and_free_focus()

        page_header = self.get_element_text(self.trip_planner_destination_page_header)
        property_location = re.split(r'[:(,\-]', page_header)[0].strip()
        header_text_elements = re.split(r'[:]', page_header, maxsplit=1)[1].strip().split()
        num_properties = header_text_elements[0]
        print(
            f"The number of properties displayed in the results page header for '{property_location}' is {num_properties}")
        return property_location, num_properties

    def get_num_listings_on_results_page(self, destination):
        location_locator = (By.XPATH,
                            f"//div[@data-testid='property-card'][.//span[contains(@data-testid, 'address') and contains(text(), '{destination}')]]"
                            )
        self.wait.until(EC.presence_of_all_elements_located(location_locator))
        location_related_property_tiles = self.driver.find_elements(*location_locator)
        num_results_listed = len(location_related_property_tiles)
        print(f"The number of property tiles labelled as within '{destination}' is {num_results_listed}")
        return num_results_listed

    def determine_property_sort_type(self, locator):
        sort_type_element = self.driver.find_element(*locator)
        sort_type_text = sort_type_element.text
        return sort_type_text

    def choose_property_sort_type(self, sorting_type):
        self.move_to_new_tab()

        try:
            calendar_picker_open = self.wait_for_element_visibility(self.calendar_date_picker_open)
            if calendar_picker_open.is_displayed():
                print(f"The calendar picker is open. Trying to close it...")
                self.scroll_to_element(self.searchbox_whole_element)
                self.click_element(self.calendar_date_searchbox)
                time.sleep(2)
                try:
                    self.wait.until(EC.invisibility_of_element_located(self.calendar_date_picker_open))
                    print(f"The calendar picker has been closed")
                except TimeoutException:
                    raise AssertionError("The calendar picker was not closed within the set time")
        except TimeoutException:
            print("The calendar picker display is not open. Continuing with test...")

        print("Waiting for sort option dropdown to display...")
        self.wait.until(EC.presence_of_element_located(self.trip_planner_sort_type))
        print("Found sort option dropdown")

        self.original_sort_type_name = self.determine_property_sort_type(self.trip_planner_sort_type)
        print(f"The starting sort type is: {self.original_sort_type_name}")

        print(f"Clicking to open sort dropdown to look for correct sort type...")
        self.click_element(self.trip_planner_sort_btn)
        time.sleep(1)

        try:
            self.wait.until(EC.presence_of_all_elements_located(self.trip_planner_sort_choice_list))
            trip_planner_sort_type_list_elements = self.driver.find_elements(*self.trip_planner_sort_choice_list_elements)

            for type in trip_planner_sort_type_list_elements:
                try:
                    sort_type_btn = type.find_element(By.XPATH, f".//button")
                    sort_type_btn_name = sort_type_btn.find_element(By.XPATH, f".//span").text

                    if sort_type_btn_name == sorting_type:
                        print(f"The chosen sort type {sort_type_btn_name} was found")
                        try:
                            sort_type_btn.click()
                            print(f"Clicked on {sort_type_btn_name} option")
                            return
                        except NoSuchElementException:
                            raise NoSuchElementException(f"Had a problem with the {type} button")
                except ValueError:
                    raise ValueError(f"Couldn't find the selected sort type {sorting_type} within the dropdown menu")

        except TimeoutException:
            raise AssertionError("Error in finding the dropdown menu options list within the set time")

        time.sleep(5)

    def verify_sort_type_changed(self, partial_expected_type, tries = 3):
        print(f"Verifying that the new property sorting type is '{partial_expected_type}'...")

        for t in range(tries):
            actual_sort_type_name = self.determine_property_sort_type(self.trip_planner_sort_type)

            if partial_expected_type in actual_sort_type_name:
                print(f"The property sorting type was found to be successfully changed to '{partial_expected_type}' in check {t + 1}")
                return True, actual_sort_type_name
            else:
                print(f"Check #{t + 1}: the sort type is still '{actual_sort_type_name}'. Waiting to recheck update in sort type...")
                time.sleep(1)

        return False, tries, actual_sort_type_name

    def collect_limited_property_results_details(self, limit):
        print(f"Collecting the first 10 properties listed and their ratings...")

        all_property_results_names = self.driver.find_elements(*self.all_trip_planner_results_names)
        first10_property_results_name_list = self.create_limited_list_of_elements(all_property_results_names, limit)
        first10_property_results_name_list_text = [el.text for el in first10_property_results_name_list]

        all_property_results_ratings = self.driver.find_elements(*self.all_trip_planner_results_ratings)
        first10_property_results_rating_list = self.create_limited_list_of_elements(all_property_results_ratings, limit)
        first10_property_results_rating_list_text = [el.text.split() for el in first10_property_results_rating_list]
        first10_property_results_rating_list_nums = list(map(lambda rate: rate[1], first10_property_results_rating_list_text))

        combined_name_rating_list = list(zip(first10_property_results_name_list_text, [float(r) for r in first10_property_results_rating_list_nums]))
        return combined_name_rating_list

    def printout_10highest_results(self):
        combined_name_rating_results = self.collect_limited_property_results_details(10)
        print("The top 10 properties and their corresponding ratings are:")

        for index, result in enumerate(combined_name_rating_results):
            print(f"#{index+1}: '{result[0]}' with a rating of {result[1]}", sep='\n')

    def filter_by_highest_review_score(self):
        self.move_to_new_tab_and_free_focus()

        print("Scrolling to Filter by: Review score section...")
        self.wait.until(EC.visibility_of_element_located(self.review_score_filter_section))
        self.scroll_to_element(self.review_score_filter_section)

        self.wait_for_element_visibility(self.review_score_filter_9plus_checkbox)
        self.click_element(self.review_score_filter_9plus_checkbox)

    def does_highest_score_filter_btn_appear(self):
        print("Checking that the highest review score filter button is displayed...")

        highest_review_score_btn_appearance = self.wait_for_element_visibility(self.highest_review_score_filter_button)
        if highest_review_score_btn_appearance.is_displayed():
            print(f"The highest review score filter button appears was found.")
            return True
        else:
            return False

    def collect_all_filter_property_results_scores(self):
        print(f"Collecting all filtered properties listed and their scores...")

        all_filtered_results_names = self.driver.find_elements(*self.all_trip_planner_results_names)
        all_filtered_results_names_list = self.create_list_of_elements(all_filtered_results_names)
        all_filtered_results_names_list_text = [f.text for f in all_filtered_results_names_list]

        all_filtered_results_scores = self.driver.find_elements(*self.all_trip_planner_results_ratings)
        all_filtered_results_scores_list = self.create_list_of_elements(all_filtered_results_scores)
        all_filtered_results_scores_list_text = [score.text.split() for score in all_filtered_results_scores_list]
        all_filtered_results_scores_list_nums = list(map(lambda scoring: scoring[1], all_filtered_results_scores_list_text))

        combined_property_score_list = list(zip(all_filtered_results_names_list_text, [float(s) for s in all_filtered_results_scores_list_nums]))
        print("After filtering, the displayed properties and their corresponding ratings are:")

        for index, result in enumerate(combined_property_score_list):
            print(f"#{index + 1}: '{result[0]}' with a rating of {result[1]}", sep='\n')

        return combined_property_score_list

    def get_all_listed_ratings_under_9(self):
        print(f"Verifying that all the resulting filtered properties have a score of 9 or higher...")
        combined_property_score_list = self.collect_all_filter_property_results_scores()

        less_than_9_properties_list = []

        for name, score in combined_property_score_list:
            if score < 9:
                less_than_9_properties_list.append((name, score))

        if len(less_than_9_properties_list) > 0:
            properties_with_lower_score = ",".join([f"'{name}' ({score})" for name, score in less_than_9_properties_list])
            raise AssertionError(f"Expected all filtered properties to score '9' or more but these properties didn't: {properties_with_lower_score}")
            return properties_with_lower_score
        else:
            return False
