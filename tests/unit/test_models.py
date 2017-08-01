import unittest
import uuid

import requests
import responses

from models import Item


class ItemTests(unittest.TestCase):

    def setUp(self):
        url = "https://abc/def/ghi?jkl=mno"
        token = "Bearer xyz"
        phone = "+0123"
        self.mock_db = unittest.mock.Mock()

        self.headers = {"Authorization": token}
        self.item = Item(url, token, phone, self.mock_db)

    def test_initialize_model_fields_with_for_first_time(self):
        url = "https://abc/def/ghi?jkl=mno"
        token = "Bearer xyz"

        self.assertEqual(url, self.item.url)
        self.assertEqual(token, self.item.token)
        self.assertEqual("+0123", self.item.phone)
        self.assertEqual(self.mock_db, self.item.db)
        self.assertEqual("YES", self.item.is_active)
        self.assertEqual(0, self.item.failed_count)
        self.assertTrue(uuid.UUID(str(self.item.id)))

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

    def test_extract_response_with_valid_data(self):
        self.item.latest_call = requests.Response()
        self.item.latest_call.json = {"k1": "abc", "Status": "PC", "k3": "def"}

        self.item.extract_status()

        self.assertEqual("PC", self.item.status)

    def test_extract_response_with_invalid_data(self):
        self.item.latest_call = requests.Response()
        self.item.latest_call.json = {"k1": "abc", "err": "PC", "k3": "def"}

        self.item.extract_status()
        self.assertEqual("error", self.item.status)
        self.assertEqual(1, self.item.failed_count)

        self.item.extract_status()
        self.assertEqual(2, self.item.failed_count)

    def test_save_item_for_initial_creation(self):
        self.item.id = str(uuid.uuid4())
        fields = ["url", "token", "phone", "failed_count", "is_active"]

        attributes = [
            {"Name": "url", "Value": self.item.url},
            {"Name": "token", "Value": self.item.token},
            {"Name": "phone", "Value": self.item.phone},
            {"Name": "failed_count", "Value": str(self.item.failed_count)},
            {"Name": "is_active", "Value": str(self.item.is_active)},
        ]

        self.item.save(fields)

        self.item.db.put_attributes.assert_called_once_with(
            item_name=str(self.item.id),
            attributes=attributes)
