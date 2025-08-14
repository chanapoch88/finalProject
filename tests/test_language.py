import pytest
import allure

from pages.language import Language

# To verify that the language window opens after press on language button
@pytest.mark.language
@allure.suite("Language Suite")
def test_language_button_opens_window_1(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    lang1 = Language(driver)
    lang1.open_language_window()
    expected_language_page_header = "Select your language"
    actual_page_header = lang1.get_language_window_title()
    assert actual_page_header == expected_language_page_header, f"The window header '{expected_language_page_header}' was expected but instead got '{actual_page_header}'"

# To verify that the main page reopens after the currency window is closed
@pytest.mark.language
@allure.suite("Language Suite")
def test_main_page_reopens_after_language_window_closed_2(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    lang2 = Language(driver)
    lang2.open_language_window()
    expected_language_page_header = "Select your language"
    actual_page_header = lang2.get_language_window_title()
    assert actual_page_header == expected_language_page_header, f"The window header '{expected_language_page_header}' was expected but instead got '{actual_page_header}'"
    lang2.close_language_window()
    expected_page_title_after_close_lang_window = "Find your next stay"
    actual_page_header = lang2.get_main_page_title()
    assert actual_page_header == expected_page_title_after_close_lang_window, f"Expected to get the main page title '{expected_page_title_after_close_lang_window}' but got '{actual_page_header}'"

# To change language type within 'Selected for you' section randomly & verify that change was made
@pytest.mark.language
@allure.suite("Language Suite")
def test_change_selected_language_randomly_and_verify_change_3(setup):
    driver = setup
    driver.get("https://www.booking.com/")
    lang3 = Language(driver)
    lang3.open_language_window()
    expected_chosen_language = lang3.select_language_by_random()
    actual_language_name = lang3.get_new_language_btn_value()
    assert expected_chosen_language in actual_language_name, \
        (f"Test failed. Language type didn't change to '{actual_language_name}', got '{actual_language_name}' instead")

# To change language type within 'All currencies' section according to text & verify change was made
@pytest.mark.language
@allure.suite("Language Suite")
def test_change_chosen_language_byText_and_verify_change_4(setup):
    driver = setup
    driver.delete_all_cookies()
    driver.get("https://www.booking.com/")
    lang4 = Language(driver)
    lang4.open_language_window()
    lang4.select_lang_type_by_text("Italiano")
    expected_selected_language = "Italiano"
    actual_displayed_language_name = lang4.get_new_language_btn_value()
    assert expected_selected_language in actual_displayed_language_name, \
        (f"Test failed. Language type didn't change to '{expected_selected_language}', got '{actual_displayed_language_name}' instead")

