import pytest
import allure

from pages.register import Register

# To verify Register button reaches sign-up page
@pytest.mark.register
@allure.suite("Register Suite")
def test_register_opens_signup_page1(setup):
    driver = setup
    reg1 = Register(driver)
    reg1.click_register_btn()
    actual_header = reg1.get_register_page_header_text()
    expected_header = "Sign in or create an account"
    assert expected_header == actual_header, f"The window header '{expected_header}' was expected but instead got '{actual_header}'"

# To verify error on signup page when press 'Continue with Email' btn with blank email field
@pytest.mark.register
@allure.suite("Register Suite")
def test_register_blank_email_error2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    reg2 = Register(driver)
    reg2.click_register_btn()
    reg2.signin_signup("")
    actual_error_msg = reg2.get_register_email_error_text()
    expected_error_msg = "Enter your email address"
    assert expected_error_msg == actual_error_msg, f"Error message mismatch. Expected to get: '{expected_error_msg}' but actually got: '{actual_error_msg}'"

# To verify error on signup page when press 'Continue' btn with invalid email
@pytest.mark.register
@allure.suite("Register Suite")
def test_register_invalid_email_error3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    reg3 = Register(driver)
    reg3.click_register_btn()
    reg3.signin_signup("chanapochgmail.com")
    actual_error_msg = reg3.get_register_email_error_text()
    expected_error_msg = "Make sure the email address you entered is correct."
    assert expected_error_msg == actual_error_msg, f"Error message is not the expected: '{expected_error_msg}'. Instead error message showed: '{actual_error_msg}'"

