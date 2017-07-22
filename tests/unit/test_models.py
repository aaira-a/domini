import unittest

import requests
import responses

from models import Item


class ItemTests(unittest.TestCase):

    def setUp(self):
        url = "https://abc/def/ghi?jkl=mno"
        token = "Bearer xyz"

        self.headers = {"Authorization": token}
        self.item = Item(url, token)

    def test_initialize_model_fields_with_for_first_time(self):
        url = "https://abc/def/ghi?jkl=mno"
        token = "Bearer xyz"

        self.assertEqual(url, self.item.url)
        self.assertEqual(token, self.item.token)
        self.assertTrue(self.item.is_active)
        self.assertEqual(0, self.item.failed_count)

    @responses.activate
    def test_fetch_from_provider_with_correct_format(self):
        responses.add(responses.GET, self.item.url,
                      adding_headers=self.headers, match_querystring=True)

        self.item.fetch_from_provider()

        request = responses.calls[0].request
        self.assertEqual(self.item.url, request.url)
        self.assertDictContainsSubset(self.headers, request.headers)

    @responses.activate
    def test_successful_fetch_from_provider_should_set_field(self):
        responses.add(responses.GET, self.item.url,
                      adding_headers=self.headers, match_querystring=True)

        self.item.fetch_from_provider()
        self.assertEqual(requests.models.Response, type(self.item.latest_call))

    @responses.activate
    def test_unsuccessful_fetch_from_provider_should_set_field(self):
        responses.add(responses.GET, self.item.url,
                      adding_headers=self.headers, match_querystring=True,
                      body=requests.exceptions.ConnectionError)

        self.item.fetch_from_provider()
        self.assertIn("failed", self.item.latest_call)
        self.assertEqual(1, self.item.failed_count)

        self.item.fetch_from_provider()
        self.assertEqual(2, self.item.failed_count)