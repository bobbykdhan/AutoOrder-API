import _thread
import os

import dotenv
import pyotp
import base64

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec





def get_code(token=None, count=None):
    if token is None:
        token = os.getenv('TOKEN')
    if count is None:
        count = int(os.getenv('COUNT'))
    dotenv.set_key(dotenv.find_dotenv(), "COUNT", str(count + 1))

    return str(pyotp.HOTP(base64.b32encode(token.encode("utf-8"))).at(count))


def login(driver, no_duo=False, username=None, password=None, url=None):
    if username is None:
        username = os.getenv("USERNAME")
    if password is None:
        password = os.getenv("PASSWORD")
    if url is not None:
        driver.get(url)

    driver.find_element(By.ID, "ritUsername").send_keys(username)
    driver.find_element(By.ID, "ritPassword").send_keys(password)
    driver.find_element(By.NAME, "_eventId_proceed").click()
    if not no_duo:
        try:
            duo(driver)
        except Exception as e:
            print("Duo failed or was not required")
            print(e)


def duo(driver):
    wait = WebDriverWait(driver, 50, poll_frequency=1)
    wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "button--link")))
    driver.find_element(By.CLASS_NAME, "button--link").click()
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "auth-method")))
    for option in driver.find_elements(By.CLASS_NAME, "auth-method"):
        if "Duo Mobile passcode" in option.text:
            option.click()
            break
    wait.until(ec.visibility_of_element_located((By.ID, "passcode-input")))
    driver.find_element(By.ID, "passcode-input").send_keys(get_code())
    driver.find_element(By.XPATH, "//*[text()='Verify']").click()
    wait.until(ec.visibility_of_element_located((By.ID, "trust-browser-button")))
    driver.find_element(By.ID, "trust-browser-button").click()



    return driver
# if __name__ == '__main__':
#     driver = create_driver()
#     x = _thread.start_new_thread(cancelFunction, (driver,))
#     loop_driver(driver)
