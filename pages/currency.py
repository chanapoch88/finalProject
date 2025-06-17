import time

from selenium.webdriver.common.by import By

from pages.base_page import Base


class Currency(Base):

    def __init__(self, driver):
        super().__init__(driver)

    currency_btn = (By.XPATH, "//button[@data-testid='header-currency-picker-trigger']")
    currency_window_title = (By.XPATH, "//div[@id='header_currency_picker']//h2")
    us_currency_selection_btn = (By.XPATH, "//*[@id='header_currency_picker']//button[.//span[contains(text(), 'Dollar')]]")
    currency_window_close_btn = (By.XPATH, "//button[@data-testid='selection-modal-close']")
    currency_btn_name = (By.XPATH, "//button[@data-testid='header-currency-picker-trigger']/span")

    def open_currency_window(self):
        self.dismiss_signin_popup()
        self.wait_and_click(self.currency_btn)

    def check_for_currency_window(self, expected_title):
        self.check_window_state(self.currency_window_title, expected_title)

    def select_currency_type(self):
        self.wait_and_click(self.us_currency_selection_btn)

    def close_currency_window(self):
        print(f"Trying to close currency window...")
        try:
            self.wait_and_click(self.currency_window_close_btn)
            print(f"Successfully closed the currency window")
            time.sleep(3)
        except Exception as e:
            print(f"Got an error while closing the currency window: {e}")
            try:
                self.click_element_withJS(self.currency_btn_name)
                print(f"Closed Currency window using click with JS")
            except Exception as JavascriptException:
                print(f"Got error when trying to perform click with JS: {JavascriptException}")
                raise

    def verify_currency_value_changed(self, exp_currency):
        actual_currency_name = self.driver.find_element(*self.currency_btn_name)
        print(f"The currency after the change is: {actual_currency_name.text}")
        assert actual_currency_name.text == exp_currency, \
            (f"Test failed. Occupancy details did not change to '{self.currency_btn_name}', got '{actual_currency_name.text}' instead")
