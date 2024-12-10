import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

@pytest.fixture(scope="module")
def driver():
    service = ChromeService(executable_path="chromedriver")
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def test_responsive_design(driver):
    driver.get("http://localhost:5000")

    # Prueba en escritorio
    driver.set_window_size(1920, 1080)
    assert driver.find_element(By.LINK_TEXT, "Login").is_displayed()

    # Prueba en tablet
    driver.set_window_size(768, 1024)
    assert driver.find_element(By.LINK_TEXT, "Login").is_displayed()

    # Prueba en móvil
    driver.set_window_size(375, 812)
    assert driver.find_element(By.LINK_TEXT, "Login").is_displayed()
