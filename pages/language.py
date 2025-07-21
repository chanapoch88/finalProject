import random
import time

from selenium.webdriver.common.by import By

from pages.base_page import Base


class Language(Base):

    def __init__(self, driver):
        super().__init__(driver)

    language_btn = (By.XPATH, "//button[@data-testid='header-language-picker-trigger']")
    set_language_label = (By.XPATH, "//button[@aria-label='Language: English (UK)'")
    language_window_title = (By.XPATH, "//div[@id='header_language_picker']//h2")
    selected_language_list = (By.XPATH, "//div[@data-testid='Suggested for you']//ul")
    all_language_list = (By.XPATH, "//div[@data-testid='All languages']//ul")
    modal_window_close_btn = (By.XPATH, "//button[@data-testid='selection-modal-close']")


    def open_language_window(self):
        self.dismiss_signin_popup()
        self.wait_and_click(self.language_btn)

    def check_for_language_window(self, expected_title):
        self.check_window_state(self.language_window_title, expected_title)

    def close_language_window(self):
        print(f"Trying to close language window...")
        try:
            self.wait_and_click(self.modal_window_close_btn)
            print(f"Successfully closed the language window")
            time.sleep(3)
        except Exception as e:
            print(f"Got an error while closing the language window: {e}")
            try:
                self.click_element_withJS(self.modal_window_close_btn)
                print(f"Closed language window using click with JS")
            except Exception as JavascriptException:
                print(f"Got error when trying to perform click with JS: {JavascriptException}")
                raise

    def select_language_by_random(self):
        self.wait_for_element_visibility(self.selected_language_list)
        selected_language_list = self.driver.find_element(*self.selected_language_list)
        selected_language_list_elements = selected_language_list.find_elements(By.TAG_NAME, "li")

        random_index = random.randint(0, len(selected_language_list_elements) - 1)
        randomly_picked_lang = selected_language_list_elements[random_index]
        random_language_name = randomly_picked_lang.text
        print(f"The randomly chosen language is: '{random_language_name}'")
        randomly_picked_lang.click()
        self.language_choice = random_language_name

    def select_lang_type_by_text(self, language_choice):
        self.wait_for_element_visibility(self.all_language_list)
        language_list = self.driver.find_element(*self.all_language_list)
        all_language_list_elements = language_list.find_elements(By.TAG_NAME, "li")

        for language_element in all_language_list_elements:
            if language_element.text != '' and language_choice in language_element.text:
                language_element.click()
                return True
        raise ValueError(f"The selection '{language_choice}' was not found")

    def verify_language_value_changed(self, exp_language):
        self.wait_for_element_visibility(self.language_btn)
        actual_language_btn = self.driver.find_element(*self.language_btn)
        actual_language_name = actual_language_btn.get_attribute("aria-label")

        print(f"After the change, the language button is set to: {actual_language_name}")
        assert exp_language in actual_language_name, \
            (f"Test failed. Language details did not change to '{self.exp_language}', got '{actual_language_name}' instead")
