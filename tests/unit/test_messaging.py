import os
import unittest
import urllib

import responses

from messaging import TwilioClient


class TwilioMessageTests(unittest.TestCase):

    def setUp(self):
        self.twilio_client = TwilioClient(
            from_=os.environ["TEST_TWILIO_FROM_NUMBER"],
            account_sid=os.environ["TEST_TWILIO_ACCOUNT_SID"],
            auth_token=os.environ["TEST_TWILIO_AUTH_TOKEN"],
        )

    @responses.activate
    def test_send_message_with_correct_format(self):
        url = (f"https://{self.twilio_client.account_sid}:" +
               f"{self.twilio_client.auth_token}" +
               f"@api.twilio.com/2010-04-01/Accounts/" +
               f"{self.twilio_client.account_sid}/Messages")

        responses.add(responses.POST, url)

        self.twilio_client.send_message("hello", "+0123")

        request = responses.calls[0].request

        expected_request_body = {
            "From": self.twilio_client.from_,
            "To": "+0123",
            "Body": "hello"
        }

        actual_request_body = dict(urllib.parse.parse_qsl(request.body))

        self.assertDictEqual(expected_request_body, actual_request_body)
