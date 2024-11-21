

# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

import os
from twilio.rest import Client



def send_sms(to, body):
    # Your Twilio credentials

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    twilio_phone_number = "+18662507453"
    # Initialize Twilio Client
    client = Client(account_sid, auth_token)

    # Send SMS
    message = client.messages.create(
        body=body,
        from_= twilio_phone_number,
        to=to,
    )

    print(f"Message sent to {to}: {message.body}")
    return message.body
