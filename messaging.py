import os

import requests


class TwilioClient(object):

    def __init__(self, from_=os.environ["TWILIO_FROM_NUMBER"],
                 account_sid=os.environ["TWILIO_ACCOUNT_SID"],
                 auth_token=os.environ["TWILIO_AUTH_TOKEN"]):

        self.from_ = from_
        self.account_sid = account_sid
        self.auth_token = auth_token

    def send_message(self, message, to):
        url = (f"https://{self.account_sid}:{self.auth_token}" +
               f"@api.twilio.com/2010-04-01/Accounts/" +
               f"{self.account_sid}/Messages")

        payload = {"From": self.from_, "To": to, "Body": message}

        return requests.post(url, data=payload)
