import pytest
import allure

from pages.language import Language

# To verify that the language window opens after press on language button
@pytest.mark.language
@allure.suite("Language Suite")
def test_language_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    lang1 = Language(driver)
    lang1.open_language_window()
    lang1.check_for_language_window("Select your language")

# To verify that the main page reopens after the currency window is closed
@pytest.mark.language
@allure.suite("Language Suite")
def test_language_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    lang2 = Language(driver)
    lang2.open_language_window()
    lang2.check_for_language_window("Select your language")
    lang2.close_language_window()
    lang2.verify_main_page_open("A place to call home")

# To change language type within 'Selected for you' section randomly & verify that change was made
@pytest.mark.language
@allure.suite("Language Suite")
def test_language_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    lang3 = Language(driver)
    lang3.open_language_window()
    lang3.select_language_by_random()
    lang3.verify_language_value_changed(lang3.language_choice)

# To change language type within 'All currencies' section according to text & verify change was made
@pytest.mark.language
@allure.suite("Language Suite")
def test_language_4(setup):
    driver = setup
    driver.delete_all_cookies()
    driver.get("https://www.booking.com/")
    lang4 = Language(driver)
    lang4.open_language_window()
    lang4.select_lang_type_by_text("Italiano")
    lang4.verify_language_value_changed("Italiano")
