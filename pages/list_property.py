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

    def get_join_listings_page_header(self):
        print("Trying to get page header after opening list property window...")
        actual_header = self.get_element_text(self.join_other_listings)
        print(f"The actual page header is '{actual_header}'.")
        return actual_header