from selenium.webdriver.common.by import By
from selenium.common import TimeoutException

from pages.base_page import Base

class Register(Base):

    def __init__(self, driver):
        super().__init__(driver)

    register_btn = (By.XPATH, '//a[@aria-label="Register an account"]')
    emailField = (By.XPATH, '//*[@type="email"]')
    signin_up_page_title = (By.XPATH, '//div[@class="page-header"]/h1')
    continue_withEmail_btn = (By.XPATH, '//button[contains(@class,"gIseXOjLVJsp5fEGivrq")]')
    email_alert = (By.ID, 'username-note')

    def click_register_btn(self):
        self.dismiss_signin_popup()
        self.wait_and_click(self.register_btn)
        print("Current URL:", self.driver.current_url)
        self.wait_for_element(self.emailField)

    # function to fill signin/signup form
    def signin_signup(self, user_email):
        self.type(self.emailField, user_email)
        self.wait_and_click(self.continue_withEmail_btn)

    def get_register_email_error_text(self):
        try:
            error_message_text = self.get_element_text(self.email_alert)
            print(f"The error received is '{error_message_text}'")
            return error_message_text

        except TimeoutException:
            return None

    def get_register_page_header_text(self):
        return super().get_page_header_text(self.signin_up_page_title)