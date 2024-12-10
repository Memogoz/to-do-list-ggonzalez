import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    service = ChromeService(executable_path="chromedriver")  # Cambia si usas otro controlador
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecuta en modo headless
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_user_registration_and_task_workflow(driver):
    driver.get("http://localhost:5000")

    # Registro de usuario
    driver.find_element(By.LINK_TEXT, "Sign In").click()
    driver.find_element(By.NAME, "user").send_keys("selenium_user")
    driver.find_element(By.NAME, "email").send_keys("selenium@example.com")
    driver.find_element(By.NAME, "password").send_keys("selenium_password")
    driver.find_element(By.XPATH, "//button[text()='Create Account']").click()
    assert "Login" in driver.page_source

    # Inicio de sesión
    driver.find_element(By.NAME, "user").send_keys("selenium_user")
    driver.find_element(By.NAME, "password").send_keys("selenium_password")
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    assert "Welcome back" in driver.page_source

    # Crear una tarea
    driver.find_element(By.NAME, "title").send_keys("Selenium Task")
    driver.find_element(By.NAME, "details").send_keys("Details for Selenium Task")
    driver.find_element(By.NAME, "priority").send_keys("1")
    driver.find_element(By.XPATH, "//button[text()='Add Task']").click()
    assert "Selenium Task" in driver.page_source

    # Editar la tarea
    driver.find_element(By.LINK_TEXT, "Edit").click()
    driver.find_element(By.NAME, "title").clear()
    driver.find_element(By.NAME, "title").send_keys("Updated Selenium Task")
    driver.find_element(By.XPATH, "//button[text()='Update Task']").click()
    assert "Updated Selenium Task" in driver.page_source

    # Eliminar la tarea
    driver.find_element(By.LINK_TEXT, "Delete").click()
    assert "Updated Selenium Task" not in driver.page_source

    # Cerrar sesión
    driver.find_element(By.LINK_TEXT, "Logout").click()
    assert "You have been logged out" in driver.page_source
