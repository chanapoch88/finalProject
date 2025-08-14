import pytest
import allure

from pages.signin import Signin

# To verify Sign-in button reaches sign-in page
@pytest.mark.signin
@allure.suite("Sign-in Suite")
def test_signin_opens_signup_page_1(setup):
    driver = setup
    sign1 = Signin(driver)
    sign1.click_signin_btn()
    actual_header = sign1.get_signin_page_header_text()
    expected_header = "Sign in or create an account"
    assert expected_header == actual_header, f"The window header '{expected_header}' was expected but instead got '{actual_header}'"

# To verify error on signin page when press 'Continue with Email' btn with blank email field
@pytest.mark.signin
@allure.suite("Sign-in Suite")
def test_signin_blank_email_error_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    sign2 = Signin(driver)
    sign2.click_signin_btn()
    sign2.signin_signup("")
    actual_error_msg = sign2.get_signup_email_error_text()
    expected_error_msg = "Enter your email address"
    assert expected_error_msg == actual_error_msg, f"Incorrect error message! Expected to get: '{expected_error_msg}' but actually got: '{actual_error_msg}'"

# To verify error on signin page when press 'Continue' btn with invalid email
@pytest.mark.signin
@allure.suite("Sign-in Suite")
def test_signin_invalid_email_error_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    sign3 = Signin(driver)
    sign3.click_signin_btn()
    sign3.signin_signup("chanapochgmail.com")
    actual_error_msg = sign3.get_signup_email_error_text()
    expected_error_msg = "Make sure the email address you entered is correct."
    assert expected_error_msg == actual_error_msg, f"Incorrect error message! Expected to get: '{expected_error_msg}' but actually got: '{actual_error_msg}'"

# To verify 'Customer terms of service' page opens when click on 'Terms & Conditions' link
@pytest.mark.signin
@allure.suite("Sign-in Suite")
def test_link_opens_terms_conditions_page_4(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    sign4 = Signin(driver)
    sign4.click_signin_btn()
    sign4.click_terms_conditions_link()
    actual_tab_header = sign4.get_service_terms_page_header_text()
    expected_tab_header = "Customer terms of service"
    assert expected_tab_header == actual_tab_header, f"Tab header is incorrect! Expected to get: '{expected_tab_header}' but instead got: '{actual_tab_header}'"

# To verify 'Customer terms of service' page opens when click on 'Terms & Conditions' link
@pytest.mark.signin
@allure.suite("Sign-in Suite")
def test_link_opens_privacy_statement_page_5(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    sign5 = Signin(driver)
    sign5.click_signin_btn()
    sign5.click_privacy_statement_link()
    actual_tab_title = sign5.get_privacy_statement_page_header_text()
    expected_tab_title = "Privacy & Cookie Statement"
    assert expected_tab_title == actual_tab_title, f"Tab title is incorrect! Expected to get: '{expected_tab_title}' but instead got: '{actual_tab_title}'"
