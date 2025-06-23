import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import Base


class BrowsePropertyType(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.category_name = "Browse by property type"
        self.chosen_category_name = None

    browse_by_property_type_section = (By.XPATH, "//div[@data-qmab-component-id='5']//h2")
    browse_by_property_type_group = (By.XPATH, "//ul[@aria-label='Browse by property type']")
    browse_by_property_type_categories = (By.XPATH, "//ul[@aria-label='Browse by property type']/li")
    browse_by_property_type_category_links = (By.XPATH, "//ul[@aria-label='Browse by property type']/li/a")
    browse_by_property_type_category_names = (By.XPATH, "//ul[@aria-label='Browse by property type']//h3")
    category_page_header = (By.TAG_NAME, "h1")
    category_page_subhead = (By.XPATH, "//h2[contains(@class, 'subtitle-text')]")
    most_booked_section = (By.XPATH, "//div[contains(@class, 'most-booked__container')]")
    first_most_booked = (By.XPATH, "//div[contains(@class, 'most-booked__container')]/div[1]")
    hotels_subhead_title = (By.XPATH, "//h2[contains(@class, 'sb-searchbox__subtitle-text')]")
    signin_banner = (By.XPATH, "//div[@class='bui-box bui-box--size-large']")
    signin_banner_close_btn = (By.XPATH, "//button[@aria-label='Close sign in banner, button']")


    def scroll_to_browse_by_property_type(self):
        self.scroll_to_element(self.browse_by_property_type_section)
        self.wait_for_element_visibility(self.browse_by_property_type_group)

    def list_browse_by_property_type(self):
        print(f"The categories listed under 'Browse by property type' are:")
        category_names = self.driver.find_elements(*self.browse_by_property_type_categories)
        self.print_list_elements(category_names)

    def count_browse_by_property_type(self):
        category_names = self.driver.find_elements(*self.browse_by_property_type_categories)
        self.count_elements(category_names, self.category_name)

    def choose_category(self, type_name):
        self.wait.until(EC.presence_of_all_elements_located(self.browse_by_property_type_categories))
        all_categories = self.driver.find_elements(*self.browse_by_property_type_categories)

        for category in all_categories:
            category_name = category.find_element(By.TAG_NAME, "h3").text
            if category_name == type_name:
                print(f"The chosen category is: {category_name}")
                category_link = category.find_element(By.TAG_NAME, "a")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", category_link)
                time.sleep(1)
                try:
                    self.wait.until(EC.element_to_be_clickable(category_link)).click()
                except Exception as e:
                    print(f"Couldn't click due to {e}, so now trying with JavaScript click...")
                    self.driver.execute_script("arguments[0].click();", category_link)

                self.chosen_category_name = category_name
                return
        raise ValueError(f"Could not find category '{type_name}'")

    def scroll_to_most_booked_section(self):
        self.scroll_to_element(self.most_booked_section)
        self.wait_for_element_visibility(self.most_booked_section)

    def close_signin_banner(self, timeout=5):
        print("Trying to close sign-in banner...")
        try:
            banner = self.wait.until(EC.presence_of_element_located(self.signin_banner))
            print("Signin banner appeared")
            try:
                close_signin_btn = self.driver.find_element(*self.signin_banner_close_btn)
                close_signin_btn.click()
                print("Signin banner was closed")
                time.sleep(2)
            except (NoSuchElementException):
                print(f"Popup appeared but the signin banner's close button wasn't found.")
        except (TimeoutException):
            print(f"The sign-in banner did not appear or disappeared before it could be dismissed.")
        except Exception as e:
            print(f"An error occurred while dismissing the popup: {e}")

    def verify_results_title_contains(self, partial_expected_header):
        watchword = self.chosen_category_name.lower()
        self.verify_partial_title(self.category_page_subhead, watchword, partial_expected_header)

    def get_details_of_1st_most_booked_listing(self, type_name):
        if type_name == "Hotels":
            time.sleep(1)
            self.close_signin_banner()
            self.wait.until(EC.presence_of_element_located(self.hotels_subhead_title))
            watchword = type_name.lower()
            partial_expected_header = "to luxury rooms and everything in between"
            self.verify_partial_title(self.hotels_subhead_title, watchword, partial_expected_header)
            print(f"The 'Hotels' category has no 'Most booked' section on its page so the test for 'Most booked' is skipped.")
            return

        self.check_window_state(self.category_page_header, type_name)
        self.scroll_to_most_booked_section()
        self.wait.until(EC.presence_of_all_elements_located(self.first_most_booked))

        first_most_booked = self.driver.find_element(*self.first_most_booked)
        first_most_booked_name = first_most_booked.find_element(By.XPATH, ".//header/a").text
        first_most_booked_place = first_most_booked.find_element(By.XPATH, ".//header/p").text
        first_most_booked_rating = first_most_booked.find_element(By.XPATH, ".//div[@class='bui-card__text']//span[@class='review-score-badge']").text

        print(f"The 1st listing for 'Most booked {self.chosen_category_name}' is {first_most_booked_name}, located in '{first_most_booked_place}', with a rating of {first_most_booked_rating}.")
