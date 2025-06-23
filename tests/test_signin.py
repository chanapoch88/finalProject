import pytest
import allure

from pages.signin import Signin

# To verify Sign-in button reaches sign-in page
@pytest.mark.signin
@allure.suite("Sign-in Suite")
def test_signin_1(setup):
    driver = setup
    sign1 = Signin(driver)
    sign1.click_signin_btn()
    sign1.check_changePage("Sign in or create an account")

# To verify error on signin page when press 'Continue with Email' btn with blank email field
@pytest.mark.signin
@allure.suite("Sign-in Suite")
def test_signin_invalid2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    sign2 = Signin(driver)
    sign2.click_signin_btn()
    sign2.signin_signup("")
    sign2.verify_error_msg("Enter your email address")

# To verify error on signin page when press 'Continue' btn with invalid email
@pytest.mark.signin
@allure.suite("Sign-in Suite")
def test_signin_invalid3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    sign3 = Signin(driver)
    sign3.click_signin_btn()
    sign3.signin_signup("chanapochgmail.com")
    sign3.verify_error_msg("Make sure the email address you entered is correct.")

# To verify 'Customer terms of service' page opens when click on 'Terms & Conditions' link
@pytest.mark.signin
@allure.suite("Sign-in Suite")
def test_terms_conditions(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    sign4 = Signin(driver)
    sign4.click_signin_btn()
    sign4.click_terms_conditions_link()
    sign4.verify_terms_conditions_page(sign4.terms_conditions_page_header,"Customer terms of service")

# To verify 'Customer terms of service' page opens when click on 'Terms & Conditions' link
@pytest.mark.signin
@allure.suite("Sign-in Suite")
def test_privacy_statement(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    sign5 = Signin(driver)
    sign5.click_signin_btn()
    sign5.click_privacy_statement_link()
    sign5.verify_terms_conditions_page(sign5.privacy_statement_page_name, "Privacy & Cookie Statement")
