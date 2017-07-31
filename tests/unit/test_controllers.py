import unittest
from unittest.mock import patch

import controllers

from query_result_fixture import results as mock_results


class ItemControllerTests(unittest.TestCase):

    def setUp(self):
        self.mock_db_instance = unittest.mock.MagicMock()
        self.mock_db_module = unittest.mock.Mock()
        self.mock_db_module.SimpleDB.return_value = self.mock_db_instance
        self.controller = controllers.ItemController(self.mock_db_module)

    def test_controller_init_should_instantiate_db(self):
        self.mock_db_module.SimpleDB.assert_called_once()
        self.assertEqual(self.controller.db, self.mock_db_instance)
        self.mock_db_instance.create_domain.assert_called_once()

    @patch('controllers.Item')
    def test_add_item_saves_correct_fields_to_model(self, mock_Item):
        self.url = "https://abc/def/ghi?jkl=mno"
        self.token = "Bearer xyz"

        self.controller.add(self.url, self.token)

        mock_Item.assert_called_with(self.url, self.token,
                                     self.mock_db_instance)
        mock_Item().save.assert_called_with(
            fields=["url", "token", "failed_count", "is_active"])

    def test_get_active_items_queries_db_with_correct_format(self):
        self.controller.get_active_items()
        self.mock_db_instance.query.assert_called_once_with("is_active", "YES")

    def test_get_active_items_hydrates_db_query_into_model(self):
        self.mock_db_instance.query.return_value = mock_results

        items = self.controller.get_active_items()

        expected_object_1 = controllers.Item(
            is_existing=True,
            id_="cd8aafae-47ad-4abf-8d51-ca51912e1936",
            url="url1",
            token="token1",
            failed_count=3,
            db=self.mock_db_instance)

        expected_object_2 = controllers.Item(
            is_existing=True,
            id_="9ac48b02-e125-4a4c-a67b-582cf87f9345",
            url="url3",
            token="token3",
            failed_count=1,
            db=self.mock_db_instance)

        self.assertEqual(2, len(items))

        self.assertEqual(expected_object_1.id, items[0].id)
        self.assertEqual(expected_object_1.url, items[0].url)
        self.assertEqual(expected_object_1.token, items[0].token)
        self.assertEqual(expected_object_1.failed_count, items[0].failed_count)

        self.assertEqual(expected_object_2.id, items[1].id)
        self.assertEqual(expected_object_2.url, items[1].url)
        self.assertEqual(expected_object_2.token, items[1].token)
        self.assertEqual(expected_object_2.failed_count, items[1].failed_count)
