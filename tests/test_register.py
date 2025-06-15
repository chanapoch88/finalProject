import pytest
import allure

from pages.register import Register

# To verify Register button reaches sign-up page
@pytest.mark.register
@allure.suite("Register Suite")
def test_register_1(setup):
    driver = setup
    reg1 = Register(driver)
    reg1.click_register_btn()
    reg1.check_changePage("Sign in or create an account")

# To verify error on signup page when press 'Continue with Email' btn with blank email field
@pytest.mark.register
@allure.suite("Register Suite")
def test_register_invalid2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    reg2 = Register(driver)
    reg2.click_register_btn()
    reg2.signin_signup("")
    reg2.verify_error_msg("Enter your email address")

# To verify error on signup page when press 'Continue' btn with invalid email
@pytest.mark.register
@allure.suite("Register Suite")
def test_register_invalid3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    reg3 = Register(driver)
    reg3.click_register_btn()
    reg3.signin_signup("chanapochgmail.com")
    reg3.verify_error_msg("Make sure the email address you entered is correct.")
