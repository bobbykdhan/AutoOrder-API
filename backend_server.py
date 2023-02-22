import time

from dotenv import load_dotenv
from fastapi import FastAPI

from image import upload_screenshot
from webdriver_handler import *

load_dotenv()

app = FastAPI()
# my_twilio.send_text("Personal Order server started", os.getenv("PHONE_NUMBER"))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/order/{selection}")
async def say_hello(selection: str):
    orderFood(selection)

@app.get("/testScreenshot")
async def testScreenshot():
    driver = create_driver(True)
    driver.get("https://www.youtube.com")
    print("Created driver")
    time.sleep(10)
    link = upload_screenshot(driver, True, True)
    print("Uploaded screenshot")
    # return {"message": "Screenshot is at: " + link}
    return {"message": "Request accepted"}

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

