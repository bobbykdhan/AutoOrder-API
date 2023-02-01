import os

from fastapi import FastAPI
import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager import *
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/order/{selection}")
async def say_hello(selection: str):
    orderFood(selection)


def orderFood(selection):
    # Initialize the Selenium WebDriver and the Wait object.

    # Navigate to the website.
    if selection == "breakfast1":
        print("pizza")
    elif selection == "breakfast2":
        print("burger")
    elif selection == "commonsBurger":
        print("burger")
    elif selection == "crossroadsBurger":
        print("burger")
    elif selection == "pasta1":
        print("pasta")
    elif selection == "pasta2":
        print()
PATH = os.getcwd() + "/chromedriver"

service = ChromeService(ChromeDriverManager().install())
# service = ChromeService(PATH)

options = webdriver.ChromeOptions()
# options.add_argument("--window-size=3000,3000")
# options.add_argument("--start-maximized")
# options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)
# wait = WebDriverWait(driver, 150, poll_frequency=1)
driver.get("google.com")
input("Press Enter to continue...")