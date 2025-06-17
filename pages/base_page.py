import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select


class Base:
    def __init__(self, driver):
        self.driver : WebDriver = driver
        self.wait = WebDriverWait(self.driver, 10)

    signin_popup_window = (By.XPATH, '//div[@class="bbe73dce14"]/div[contains(@class, "a9f1d9ba2c")]')
    signin_popup_dismiss_btn = (By.XPATH, '//button[@aria-label="Dismiss sign-in info."]')
    main_page_title = (By.XPATH, "//span[@data-testid='herobanner-title1']")

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

    def type(self, locators, text):
        element = self.driver.find_element(*locators)
        element.click()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        time.sleep(0.5)
        element.send_keys(text)

    def select_option(self, locator, option):
        element = Select(self.driver.find_element(*locator))
        element.select_by_value(str(option))

    def get_element_text(self, locator):
        element = self.wait_for_element(locator)
        return element.text

    def dismiss_signin_popup(self, timeout=5):
        print("Trying to dismiss sign-in popup")
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

    def verify_main_page_open(self, expected_title):
        try:
            assert self.check_window_state(self.main_page_title, expected_title), \
                "Expected to get the main page but failed"
        except AssertionError as e:
            raise AssertionError(f"Cannot find main page title: {e}")

    def verify_page_title(self, locator, expected_title):
        actual_window_title = self.get_element_text(locator)
        print(f"The current window is '{actual_window_title}'")
        assert expected_title == actual_window_title, f"The window title '{expected_title}' was expected but instead got '{actual_window_title}'"

    def check_window_state(self, locator, expected_title):
        self.wait_for_element_visibility(locator)
        self.verify_page_title(locator, expected_title)
        return True