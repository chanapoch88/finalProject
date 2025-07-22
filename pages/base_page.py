import time
from operator import itemgetter

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    ElementNotInteractableException
from selenium.webdriver.support.ui import Select


class Base:
    def __init__(self, driver):
        self.driver : WebDriver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.main_page = driver.current_window_handle

    signin_popup_window = (By.XPATH, '//div[@class="bbe73dce14"]/div[contains(@class, "a9f1d9ba2c")]')
    signin_popup_dismiss_btn = (By.XPATH, '//button[@aria-label="Dismiss sign-in info."]')
    main_page_title = (By.XPATH, "//span[@data-testid='herobanner-title1']")
    main_page_body = (By.TAG_NAME, 'body')

    def wait_for_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_element_visibility(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_and_click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        time.sleep(1)

    def click_element(self, locators):
        self.driver.find_element(*locators).click()
        time.sleep(1)

    def click_element_withJS(self, locators):
        element = self.driver.find_element(*locators)
        self.driver.execute_script("arguments[0].click();", element)

    def clear(self, locators):
        self.driver.find_element(*locators).clear()

    def check_for_text_and_clear(self, element):
        try:
            print("Checking if text field is empty...")
            text_in_field = element.get_attribute("value").strip()
            if text_in_field == "":
                print("Text field has no text so will skip clearing action")
                return

            print("Trying to clear text simply...")
            element.clear()

            print("Checking if field has been emptied of text...")
            if element.get_attribute("value").strip() != "":
                print("Field still has text. Deleting now with special keys..")
                element.send_keys(Keys.CONTROL + "a")
                element.send_keys(Keys.DELETE)
        except (TimeoutException, StaleElementReferenceException, ElementNotInteractableException) as e:
            print(f"Could not clear text field for {element} due to '{e}'")
            raise

    def type(self, locators, text):
        element = self.driver.find_element(*locators)
        element.click()
        self.check_for_text_and_clear(element)
        time.sleep(0.5)
        element.send_keys(text)

    # for selecting only elements within select tags
    def select_option(self, locator, option):
        element = Select(self.driver.find_element(*locator))
        element.select_by_value(str(option))

    def get_element_text(self, locator):
        element = self.wait_for_element(locator)
        return element.text

    def dismiss_signin_popup(self, timeout=5):
        print("Trying to dismiss sign-in popup...")
        try:
            popup = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.signin_popup_window))
            print("Popup appeared")
            try:
                dismiss_popup_btn = self.driver.find_element(*self.signin_popup_dismiss_btn)
                dismiss_popup_btn.click()
                print("Popup was dismissed")
                time.sleep(2)
            except (NoSuchElementException):
                print(f"Popup appeared but could not find popup's dismiss button.")
        except (TimeoutException):
            print(f"The sign-in popup did not appear or disappeared before it could be dismissed.")
        except Exception as e:
            print(f"An error occurred while dismissing the popup: {e}")

    # When focus locks onto specific area on page, this releases focus to overall page body
    def click_to_release_focus(self):
        self.driver.find_element(*self.main_page_body).click()
        time.sleep(1)

    def scroll_to_element(self, locator):
        if isinstance(locator, tuple):
            self.wait_for_element_visibility(locator)
            element = self.driver.find_element(*locator)
        else:
            element = locator
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def move_to_new_tab(self):
        print("Checking current number of tab windows...")
        current_tabs = self.driver.window_handles
        if len(current_tabs) > 1:
            self.driver.switch_to.window(self.main_page)
            self.driver.close()

        print("Attempting to move to new tab window...")
        all_tabs = self.driver.window_handles
        for tab in all_tabs:
            if tab != self.main_page:
                self.driver.switch_to.window(tab)
                break
        time.sleep(2)

    def return_to_main_page(self):
        print("Returning to main page window...")
        self.driver.close()
        self.driver.switch_to.window(self.main_page)

    def create_list_of_elements(self, elements):
        element_list = []
        for element in elements:
            element_list.append(element)
        return element_list

    def create_limited_list_of_elements(self, elements, limit):
        element_list = []
        for element in elements:
            if len(element_list) < limit:
                element_list.append(element)
        return element_list

    def print_list_elements(self, elements):
        for index, element in enumerate(elements):
            if index < len(elements) - 1:
                print(f"{element.text}", end=", ")
            else:
                print(f"and {element.text}", end="")

    def count_elements(self, element_list, category_name):
        element_count = len(element_list)
        print(f"\nThere are a total of {element_count} listings in the section '{category_name}'.")

    def compare_lists_highest_value(self, list1, list2, value_type):
        # make a combined list from 2 passed lists
        combined_list = list(zip([l.text for l in list1], [float(l.text) for l in list2]))

        # find the tuple (name, rating_value) in combined list with highest rating using max() and itemgetter()
        # itemgetter() is operator module function that collects items from an iterable object from the index or key
        highest_value_item = max(combined_list, key = itemgetter(1))
        print(f"The highest {value_type} is {highest_value_item[1]} and it belongs to '{highest_value_item[0]}'.")

    def choose_from_elements_by_text(self, elements, text):
        list_of_elements = self.create_list_of_elements(elements)
        for element in list_of_elements:
            if element.text == text:
                print(f"The chosen category is: {element.text}")
                return element
        raise ValueError(f"No element with text {text} was found.")

    def verify_main_page_open(self, expected_title):
        try:
            assert self.check_window_state(self.main_page_title, expected_title), \
                "Expected to get the main page but failed"
        except AssertionError as e:
            raise AssertionError(f"Cannot find page title: {e}")

    def verify_page_header(self, locator, expected_title):
        actual_window_header = self.get_element_text(locator)
        print(f"The current window is '{actual_window_header}'")
        assert expected_title == actual_window_header, f"The window header '{expected_title}' was expected but instead got '{actual_window_header}'"

    def verify_partial_title(self, locator, watchword, partial_expected_header):
        print(f"watchword: {watchword}, partial expected header: {partial_expected_header}")
        actual_header = self.get_element_text(locator)

        assert watchword in actual_header and partial_expected_header in actual_header, \
        f"'Expected to get both {watchword} and {partial_expected_header}' in the header but instead got '{actual_header}'"

        print(f"Test passed! The word '{watchword}' and the partial expected text '{partial_expected_header}' both appear in the actual text '{actual_header}.")

    def check_window_state(self, locator, expected_title):
        self.wait_for_element_visibility(locator)
        self.verify_page_header(locator, expected_title)
        return True

    # Created to resolve an issue with category types sometimes changing for different runs, probably due to geolocation dependence
    def test_category_with_fallback(self, items_list: list[dict]):
        for item in items_list:
            try:
                self.choose_trip_plan_category(item["category"])
                self.choose_trip_destination(item["destination"])
                return
            except ValueError as e:
                print(f"Test failed with '{item["category"]}/{item["destination"]}' due to '{e}'")
                continue
        raise AssertionError("No valid category/destination combination was found")

