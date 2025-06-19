from selenium.webdriver.common.by import By

from pages.base_page import Base


class ListProperty(Base):

    def __init__(self, driver):
        super().__init__(driver)


    list_property_btn = (By.XPATH, "//a[@data-testid='header-custom-action-button']")
    join_other_listings = (By.XPATH, "//div[@class='c86bf723bf']")

    def release_register_focus(self):
        self.click_to_release_focus()

    def open_list_property_window(self):
        self.dismiss_signin_popup()
        self.wait_and_click(self.list_property_btn)
        self.release_register_focus()

    def verify_join_listings_page(self, watchword, partial_expected_text):
        self.verify_title_contains(self.join_other_listings, watchword, partial_expected_text)