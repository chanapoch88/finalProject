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
    verify_email_page_title = (By.XPATH, '//h1[contains(@class, "nw-step-header")]')


    def click_register_btn(self):
        self.dismiss_signin_popup()
        self.wait_and_click(self.register_btn)
        print("Current URL:", self.driver.current_url)
        self.wait_for_element(self.emailField)

    # function to fill signin/signup form
    def signin_signup(self, user_email):
        self.actual_error_message = None
        self.type(self.emailField, user_email)
        self.wait_and_click(self.continue_withEmail_btn)
        try:
            error_message_text = self.get_element_text(self.email_alert)
            self.actual_error_message = error_message_text
            print(f"The error received is '{self.actual_error_message}'")
        except TimeoutException:
            self.actual_error_message = None

    def check_changePage(self, pageHeader):
        actualPage = self.get_element_text(self.signin_up_page_title)
        print(f"The current page is '{actualPage}'")
        assert pageHeader == actualPage, f"Page header '{pageHeader}' was expected but instead got '{actualPage}'"

    def verify_error_msg(self, expected_error_msg):
        assert expected_error_msg == self.actual_error_message, f"Error message mismatch. Expected to get: '{expected_error_msg}' but actually got: '{self.actual_error_message}'"
