import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import Base

class StaysSearch(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.destination = None
        self.initial_occupancy_text = None

    destination_field = (By.ID, ":rh:")
    open_calendar = (By.XPATH, "//button[@data-testid='searchbox-dates-container']")
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

    def type_destination(self, destination):
            time.sleep(2)
            self.destination = None
            self.dismiss_signin_popup()

            self.wait.until(EC.element_to_be_clickable(self.destination_field))

            self.wait_and_click(self.destination_field)
            self.type(self.destination_field, destination)
            self.destination = destination
            return self.destination
            time.sleep(3)

    def choose_start_date(self):
        self.wait_and_click(self.open_calendar)
        possible_start_dates = []
        starting_dates = self.driver.find_elements(*self.all_start_dates)

        for s_date in starting_dates:
            if s_date.get_attribute("aria-hidden") != 'true' and s_date.get_attribute("aria-disabled") != 'true':
                possible_start_dates.append(s_date.text)

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

    def check_occupancy(self):
        occupant_details = self.driver.find_elements(*self.occupancy_summary)
        if occupant_details:
            self.initial_occupancy_text = occupant_details[0].text
            print(f"The default occupancy is set to: {self.initial_occupancy_text}")

    def click_search_btn(self):
        self.wait_and_click(self.search_btn)

    def verify_results_title_contains(self, partial_expected_header):
        watchword = self.destination
        self.verify_partial_title(self.search_results_page_header, watchword, partial_expected_header)