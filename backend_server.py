import time

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from image import upload_screenshot
from order_manager import *
from webdriver_handler import *

load_dotenv()

app = FastAPI()

# my_twilio.send_text("Personal Order server started")

global driver

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/demoOrder")
async def demoOrder():
    driver = create_driver()
    wait = WebDriverWait(driver, 150, poll_frequency=1)
    # Opens the ondemand website
    driver.get("https://ondemand.rit.edu/")
    selectStore(driver, "Sol's")
    items = selectCategory(driver, "Beverages")
    selectedItems = []
    selectedItems.append(select_item(items, "Aquafina Water 20 oz"))
    selectedItems.append(select_item(items, "Schweppes Ginger Ale"))

    for item in selectedItems:
        addToCart(driver, items, item, {}, "Look how cool I am")

    items = selectCategory(driver, "Ice Cream")
    selectedItems = []
    addToCart(driver, items, select_item(items, "Shake"), {"Shake Choices": "Strawberry"}, "Look how cool I am")

    other_open_login(driver)
    sign_in(driver)
    wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "cart-icon")))
    driver.find_element(By.CLASS_NAME, "cart-icon").click()

    return {"message": "Done with demo order"}


@app.get("/quitDriver")
async def quitDriver():
    driver.quit()
    return {"message": "Driver quit"}


@app.get("/order/{selection}")
async def say_hello(selection: str):
    orderFood(selection)


@app.get("/testScreenshot")
async def testScreenshot():
    driver = create_driver()
    driver.get("https://www.youtube.com")
    print("Created driver")
    time.sleep(5)
    link = upload_screenshot(driver, True, True)
    print("Uploaded screenshot")
    return {"message": "Screenshot is at: " + link}

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

#TODO make this work

# @app.get('/sms')
# @app.post("/sms")
# async def root(request: Request):
#     """Respond to incoming calls with a simple text message."""
#     # Start our TwiML response
#     # resp = MessagingResponse()
#     #
#     # # Add a message
#     # resp.message("The Robots are coming! Head for the hills!")
#     #
#     # print(str(resp))
