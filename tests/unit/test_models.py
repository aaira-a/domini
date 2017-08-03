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

    def test_initialize_model_fields_for_first_time(self):
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

        self.item.fetch_status_from_provider()

        request = responses.calls[0].request
        self.assertEqual(self.item.url, request.url)
        self.assertDictContainsSubset(self.headers, request.headers)

    @responses.activate
    def test_successful_fetch_from_provider_should_return_status(self):
        responses.add(responses.GET, self.item.url,
                      json={"k1": "abc", "Status": "PC", "k3": "def"},
                      adding_headers=self.headers, match_querystring=True)

        status = self.item.fetch_status_from_provider()
        self.assertEqual("PC", status)

    @responses.activate
    def test_unsuccessful_fetch_from_provider_should_return_error(self):
        responses.add(responses.GET, self.item.url,
                      json={"k1": "abc", "err": "PC", "k3": "def"},
                      adding_headers=self.headers, match_querystring=True)

        status = self.item.fetch_status_from_provider()
        self.assertEqual("error", status)

    @responses.activate
    def test_connection_error_fetch_from_provider_should_return_error(self):
        responses.add(responses.GET, self.item.url,
                      adding_headers=self.headers, match_querystring=True,
                      body=requests.exceptions.ConnectionError)

        status = self.item.fetch_status_from_provider()
        self.assertEqual("error", status)

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

    def test_increment_error_count(self):
        self.assertEqual(0, self.item.failed_count)
        self.item.increment_failed_count()
        self.item.increment_failed_count()
        self.assertEqual(2, self.item.failed_count)
