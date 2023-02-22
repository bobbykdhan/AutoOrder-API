import os

from dotenv import load_dotenv
from imgurpython import ImgurClient

import my_twilio
from webdriver_handler import create_driver

"""
Code adapted from
https://github.com/skorokithakis/imgur-uploader
"""


def get_config():
    client_id = os.environ.get("IMGUR_API_ID")
    client_secret = os.environ.get("IMGUR_API_SECRET")

    client_id = client_id
    client_secret = client_secret

    if not (client_id and client_secret):
        return {}

    data = {"id": client_id, "secret": client_secret}
    return data


def upload_image(image, debug=False):
    """Uploads image files to Imgur"""

    config = get_config()

    if not config:
        print("Cannot upload - could not find IMGUR_API_ID or " "IMGUR_API_SECRET environment variables or config file")

        config = get_config()
        if not config:
            return ""

    response = ImgurClient(config["id"], config["secret"]).upload_from_path(image, anon=True)

    return response['link']


def upload_screenshot(driver, new_pic=True, send_text=False, filename=None, path=None):
    if filename is None:
        filename = "screen"
    if path is None:
        if not os.path.exists(os.path.join(os.getcwd(), "screenshots")):
            os.mkdir(os.path.join(os.getcwd(), "screenshots/"), exist_ok=True)
        path = os.path.join(os.getcwd(), "screenshots/" + filename + ".png")
    if new_pic:
        path = take_screenshot(driver, filename, path)
    link = upload_image(path)
    if send_text:
        my_twilio.send_text(("The link is: " + link), os.getenv("PHONE_NUMBER"))
    if link == "":
        return "Error"
    return link


def take_screenshot(driver, filename=None, path=None):
    if filename is None:
        filename = "screen"
    if path is None:
        if not os.path.exists(os.path.join(os.getcwd(), "screenshots")):
            os.mkdir(os.path.join(os.getcwd(), "screenshots/"))
        path = os.path.join(os.getcwd(), "screenshots/" + filename + ".png")
    driver.save_screenshot(path)
    return path


if __name__ == '__main__':
    load_dotenv()
    driver = create_driver()
    print(upload_screenshot(driver, False, False))
