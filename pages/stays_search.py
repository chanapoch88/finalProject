import time
import random
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, TimeoutException

from pages.base_page import Base

class StaysSearch(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.destination = None
        self.initial_occupancy_text = None

    destination_field = (By.ID, ":rh:")
    click_field_opens_calendar = (By.XPATH, "//button[@data-testid='searchbox-dates-container']")
    calendar_data_picker_searchbox = (By.XPATH, "//div[@data-testid='searchbox-datepicker-calendar']")
    search_destination_autocomplete_result_list = (By.XPATH, "//div[@data-testid='autocomplete-results-options']/ul")
    search_destination_autocomplete_result_elements = (By.XPATH, "//div[@data-testid='autocomplete-results-options']/ul/li")
    search_destination_autocomplete_result_names = (By.XPATH, "//div[@data-testid='autocomplete-results-options']/ul/li//div[@class='b08850ce41 d704c15739']")
    all_start_dates = (By.XPATH, "//*[@id='calendar-searchboxdatepicker']//div[1]/table/tbody//td/span")
    current_date = (By.XPATH, "//*[@id='calendar-searchboxdatepicker']//div[@class='d7bd90e008']/table/tbody//td/span[contains(@class, 'd9382a910a')]")
    all_end_dates = (By.XPATH, "//*[@id='calendar-searchboxdatepicker']//div[2]/table/tbody//td/span")
    start_date = (By.XPATH, "//span[@data-testid='date-display-field-start']")
    end_date = (By.XPATH, "//span[@data-testid='date-display-field-end']")
    occupants_field = (By.XPATH, "//button[@data-testid='occupancy-config']")
    child_increase_btn = (By.XPATH, "//div[@data-testid='occupancy-popup']//div[@class='e484bb5b7a'][2]//button[contains(@class, 'aaf9b6e287')]")
    age_field = (By.XPATH, "//div[@data-testid='kids-ages-select']")
    age_options = (By.XPATH, "//div[@data-testid='kids-ages-select']//select[@name='age']")
    occupancy_summary = (By.XPATH, "//button[@data-testid='occupancy-config']/span[contains(@class, 'be2db1c937')]")
    occupancy_done_btn = (By.XPATH, "//div[@data-testid='occupancy-popup']/button[contains(@class, 'bbf83acb81')]")
    search_btn = (By.CSS_SELECTOR, "button[type='submit']")
    search_results_page_header = (By.TAG_NAME, "h1")
    open_map_search_field = (By.XPATH, "//input[@aria-label='Search on map']")
    map_view_close_btn = (By.XPATH, "//button[@aria-label='Close map']")
    search_results_page_header = (By.TAG_NAME, "h1")

    def type_destination(self, destination):
            time.sleep(2)
            self.destination = None
            self.dismiss_signin_popup()

            self.wait_and_click(self.destination_field)
            self.type(self.destination_field, destination)
            self.destination = destination
            return self.destination
            time.sleep(3)

    def type_partial_destination(self, part_destination):
        time.sleep(2)
        self.destination = None
        self.dismiss_signin_popup()

        self.wait_and_click(self.destination_field)
        time.sleep(2)
        self.type(self.destination_field, part_destination)

        self.wait_for_element_visibility(self.search_destination_autocomplete_result_list)
        time.sleep(2)

        try:
            autocomplete_destination_list_elements = self.driver.find_elements(*self.search_destination_autocomplete_result_elements)
            if not autocomplete_destination_list_elements:
                raise ValueError("No autocomplete suggestions were displayed")
        except Exception as e:
            print(f"Could not find any autocomplete suggestions: {e}")
            raise

        random_index = random.randint(0, len(autocomplete_destination_list_elements) - 1)
        randomly_picked_destination = autocomplete_destination_list_elements[random_index]

        try:
            random_destination_name = randomly_picked_destination.find_element(By.XPATH, f".//div[@class='b08850ce41 d704c15739']").text
            print(f"The randomly chosen destination is: '{random_destination_name}'")

            chosen_destination_btn = randomly_picked_destination.find_element(By.XPATH, f".//div[@role='button']")
            chosen_destination_btn.click()
        except Exception as e:
            print(f"Was unable to click on the randomly chosen autocomplete destination option: {e}")
            raise

        self.destination = re.split(r'[:(,\-]', random_destination_name)[0].strip()
        time.sleep(1)
        return self.destination

    def choose_start_date(self):
        print("Trying to open calendar and choose start date")
        self.wait_and_click(self.click_field_opens_calendar)
        possible_start_dates = []
        starting_dates = self.driver.find_elements(*self.all_start_dates)

        for s_date in starting_dates:
            if s_date.get_attribute("aria-hidden") != 'true' and s_date.get_attribute("aria-disabled") != 'true':
                possible_start_dates.append(s_date.text)

        self.wait_for_clickable_element(self.current_date)
        self.click_element(self.current_date)
        time.sleep(2)

        chosen_start = self.driver.find_element(*self.start_date).text
        print(f"The chosen start date is {chosen_start}.")

    def choose_end_date(self):
        possible_end_dates = []
        possible_end_date_texts = []
        ending_dates = self.driver.find_elements(*self.all_end_dates)

        for e_date in ending_dates:
            if e_date.get_attribute("aria-hidden") != 'true' and e_date.get_attribute("aria-disabled") != 'true':
                possible_end_dates.append(e_date)
                possible_end_date_texts.append(e_date.text)

        first_active_date_2nd_month = possible_end_dates[0]
        first_active_date_2nd_month.click()

        chosen_end = self.driver.find_element(*self.end_date).text
        print(f"The chosen end date is {chosen_end}.")

    def choose_random_start_date(self):
        print("Trying to choose random start date...")

        try:
            calendar_elements = self.driver.find_elements(*self.calendar_data_picker_searchbox)

            if calendar_elements:
                print("Calendar is currently open")
            else:
                print("Calendar is not yet open. Clicking to open...")
                self.wait_and_click(self.click_field_opens_calendar)
                self.wait_for_element_visibility(self.calendar_data_picker_searchbox)
                print("Calendar was opened successfully")
        except Exception as e:
            print(f"There was an error opening the calendar: {e}")

            try:
                print("Retrying to open calendar...")
                self.wait_and_click(self.click_field_opens_calendar)
                self.wait_for_element_visibility(self.calendar_data_picker_searchbox)
                print("Calendar opened after retry")
            except Exception:
                print("Calendar picker could not be opened")
                raise

        time.sleep(1)

        possible_start_dates = []
        starting_dates = self.driver.find_elements(*self.all_start_dates)

        for rs_date in starting_dates:
            if rs_date.get_attribute("aria-hidden") != 'true' and rs_date.get_attribute("aria-disabled") != 'true':
                possible_start_dates.append(rs_date)

        try:
            random_start_index = random.randint(0, len(possible_start_dates) - 1)
            randomly_picked_start_date = possible_start_dates[random_start_index]

            # add to following an additional condition where len(possible_start_dates) > 1
            if randomly_picked_start_date == self.current_date:
                randomly_picked_start_date += 1
            else:
                pass
            randomly_picked_start_date.click()
        except (IndexError, ValueError):
            print("Could not find any start dates.")
            raise

        time.sleep(2)
        chosen_start = self.driver.find_element(*self.start_date).text
        print(f"The chosen start date is {chosen_start}.")

    def choose_random_end_date(self):
        print("Trying to choose random end date...")
        possible_end_dates = []
        possible_end_date_texts = [] # is this needed?
        ending_dates = self.driver.find_elements(*self.all_end_dates)

        for re_date in ending_dates:
            if re_date.get_attribute("aria-hidden") != 'true' and re_date.get_attribute("aria-disabled") != 'true':
                possible_end_dates.append(re_date)
                possible_end_date_texts.append(re_date.text) # is this needed?

        random_end_index = random.randint(0, len(possible_end_dates) - 1)
        randomly_picked_end_date = possible_end_dates[random_end_index]

        randomly_picked_end_date.click()
        time.sleep(1)

        chosen_end = self.driver.find_element(*self.end_date).text
        print(f"The chosen end date is {chosen_end}.")

    def check_occupancy(self):
        occupant_details = self.driver.find_elements(*self.occupancy_summary)
        if occupant_details:
            self.initial_occupancy_text = occupant_details[0].text
            print(f"The default occupancy is set to: {self.initial_occupancy_text}")

    def click_search_btn(self):
        self.wait_and_click(self.search_btn)

    def check_for_map_view(self):
        print("Checking for opened map and, if found, trying to close it...")
        try:
            map_view = self.wait_for_element_visibility(self.open_map_search_field)
            print("Open map view is displayed")
            try:
                close_map_btn = self.wait_for_element_visibility(self.map_view_close_btn)
                close_map_btn.click()
                print("Open map view was closed")
                time.sleep(2)
            except (NoSuchElementException):
                print(f"Map view was displayed but its close button couldn't be found.")
        except (TimeoutException):
            print(f"The open map view did not appear or disappeared before it could be closed.")
        except Exception as e:
            print(f"While closing the map view, an error occurred: {e}")

    def verify_results_title_contains(self, partial_expected_header):
        watchword = self.destination
        self.verify_partial_title(self.search_results_page_header, watchword, partial_expected_header)