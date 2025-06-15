import pytest
import allure
from selenium import webdriver

driver = None

def pytest_exception_interact(report):
    if report.failed:
        global driver
        allure.attach(body=driver.get_screenshot_as_png(), name="screenshot",
        attachment_type=allure.attachment_type.PNG)

@pytest.fixture(scope="session", autouse=True)
def setup():
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.booking.com/")
    yield driver
    driver.quit()