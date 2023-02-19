import os
from dotenv import load_dotenv
from imgurpython import ImgurClient

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
    return None

    client = ImgurClient(config["id"], config["secret"])

    response = client.upload_from_path(image, anon=True)

    return response['link']




if __name__ == "__main__":
    load_dotenv()
    print("The link is" + upload_image("/Users/bobby/Documents/Projects/personalOrder/hi.png"))

