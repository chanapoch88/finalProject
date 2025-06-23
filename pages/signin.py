from selenium.webdriver.common.by import By
from selenium.common import TimeoutException

from pages.base_page import Base

class Signin(Base):

    def __init__(self, driver):
        super().__init__(driver)

    signin_btn = (By.XPATH, "//a[@aria-label='Sign in']")
    emailField = (By.XPATH, "//*[@type='email']")
    signin_up_page_title = (By.XPATH, "//div[@class='page-header']/h1")
    continue_withEmail_btn = (By.XPATH, "//button[contains(@class,'gIseXOjLVJsp5fEGivrq')]")
    email_alert = (By.ID, "username-note")
    terms_conditions_link = (By.XPATH, "//div[@class='account-access__footer']//a[.//span[contains(text(), 'Terms & Conditions')]]")
    terms_conditions_page_header = (By.TAG_NAME, "h1")
    privacy_statement_link = (By.XPATH, "//div[@class='account-access__footer']//a[.//span[contains(text(), 'Privacy Statement')]]")
    privacy_statement_page_name = (By.XPATH, "//div[@id='privacy-statement']/div")


    def click_signin_btn(self):
        self.dismiss_signin_popup()
        self.wait_and_click(self.signin_btn)
        print("Current URL:", self.driver.current_url)
        self.wait_for_element(self.emailField)

    # fills in signin/signup form
    def signin_signup(self, user_email):
        self.actual_error_message = None
        self.type(self.emailField, user_email)
        self.wait_and_click(
            self.continue_withEmail_btn)
        try:
            error_message_text = self.get_element_text(self.email_alert)
            self.actual_error_message = error_message_text
            print(f"The error received is '{self.actual_error_message}'")
        except TimeoutException:
            self.actual_error_message = None

    def check_changePage(self, expected_signin_header):
        self.verify_page_header(self.signin_up_page_title, expected_signin_header)

    def verify_error_msg(self, expected_error_msg):
        assert expected_error_msg == self.actual_error_message, f"Incorrect error message! Expected to get: '{expected_error_msg}' but actually got: '{self.actual_error_message}'"

    def click_terms_conditions_link(self):
        self.wait_and_click(self.terms_conditions_link)

    def click_privacy_statement_link(self):
        self.wait_and_click(self.privacy_statement_link)

    def verify_terms_conditions_page(self, tab_name, expected_tab_header):
        self.move_to_new_tab()
        self.verify_page_header(tab_name, expected_tab_header)
        self.return_to_main_page()
