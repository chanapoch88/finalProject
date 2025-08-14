import time

from selenium.webdriver.common.by import By

from pages.base_page import Base


class Currency(Base):

    def __init__(self, driver):
        super().__init__(driver)

    currency_btn = (By.XPATH, "//button[@data-testid='header-currency-picker-trigger']")
    currency_window_title = (By.XPATH, "//div[@id='header_currency_picker']//h2")
    us_currency_selection_btn = (By.XPATH, "//*[@id='header_currency_picker']//button[.//span[contains(text(), 'Dollar')]]")
    all_currency_listing = (By.XPATH, "//div[@data-testid='All currencies']//ul[contains(@class, 'f7aa4721a5')]")
    currency_window_close_btn = (By.XPATH, "//button[@data-testid='selection-modal-close']")
    currency_btn_name = (By.XPATH, "//button[@data-testid='header-currency-picker-trigger']/span")

    def open_currency_window(self):
        self.dismiss_signin_popup()
        self.wait_and_click(self.currency_btn)

    def get_currency_window_title(self):
        self.wait_for_element_visibility(self.currency_window_title)
        actual_currency_window_header = self.get_element_text(self.currency_window_title)
        print(f"The current window is '{actual_currency_window_header}'")
        return actual_currency_window_header

    def select_us_currency_type(self):
        self.wait_and_click(self.us_currency_selection_btn)

    def select_currency_type_by_text(self, currency_choice):
        self.wait_for_element_visibility(self.all_currency_listing)
        currencies_list = self.driver.find_element(*self.all_currency_listing)
        all_currencies_list_elements = currencies_list.find_elements(By.TAG_NAME, "li")

        for currency_element in all_currencies_list_elements:
            if currency_element.text != '' and currency_choice in currency_element.text:
                currency_element.click()
                return True
        raise ValueError(f"The selection '{currency_choice}' was not found")

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

    def get_new_currency_value(self):
        self.wait_for_element_visibility(self.currency_btn_name)
        actual_currency_btn_name = self.driver.find_element(*self.currency_btn_name)
        actual_currency_btn_name_text = actual_currency_btn_name.text
        print(f"The currency button after the change is set to: {actual_currency_btn_name_text}")
        return actual_currency_btn_name_text