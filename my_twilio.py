import os

import dotenv
from twilio.rest import Client

dotenv.load_dotenv()


def send_text(message, phone_number=os.environ['PHONE_NUMBER']):
    if int(os.environ['DEBUG']):
        auth_token = os.environ['TWILIO_TEST_TOKEN']
    else:
        auth_token = os.environ['TWILIO_AUTH_TOKEN']

    if phone_number is None:
        phone_number = os.environ['PHONE_NUMBER']

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=message,
        from_='+1' + os.environ['TWILIO_PHONE_NUMBER'],
        to='+1' + phone_number
    )
    return message.sid

def handle_message():
    pass

def cancel_order(driver):
    pass

def failed_order(driver,reason):
    pass

def repeat_order(driver):
    pass