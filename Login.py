import base64
import os

import dotenv

import pyotp as pyotp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as ec
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager

service = ChromeService(ChromeDriverManager(path=r"Drivers").install())
options = webdriver.ChromeOptions()

# service = ChromeService(PATH)

# options.add_argument("--start-maximized")
options.add_argument("--window-size=600,1000")
# options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)


def get_code(token=None, count=None):
    if token is None:
        token = os.getenv('TOKEN')
    if count is None:
        count = int(os.getenv('COUNT'))
    dotenv.set_key(dotenv.find_dotenv(), "COUNT", str(count + 1))

    return str(pyotp.HOTP(base64.b32encode(token.encode("utf-8"))).at(count))


def login(username, password, driver,url=None):

    if url is not None:
        driver.get(url)

    driver.find_element(By.ID, "ritUsername").send_keys(username)
    driver.find_element(By.ID, "ritPassword").send_keys(password)
    driver.find_element(By.NAME, "_eventId_proceed").click()
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




load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
url = " https://mycourses.rit.edu/Shibboleth.sso/Login?entityID=https%3A%2F%2Fshibboleth.main.ad.rit.edu%2Fidp%2Fshibboleth&target=https%3A%2F%2Fmycourses.rit.edu%2Fd2l%2FshibbolethSSO%2Flogin.d2l%3Ftarget%3D%252Fd2l%252Fhome"

login(url, username, password, driver)
input("Press Enter to continue...")