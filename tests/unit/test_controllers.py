import unittest
from unittest.mock import patch

import controllers


class ItemControllerTests(unittest.TestCase):

    @patch('controllers.Item')
    def test_add_item_saves_correct_fields_to_model(self, mock_Item):
        self.url = "https://abc/def/ghi?jkl=mno"
        self.token = "Bearer xyz"

        controllers.ItemController.add(self.url, self.token)

        mock_Item.assert_called_with(self.url, self.token)
        mock_Item().save.assert_called_with(
            fields=["url", "token", "failed_count", "is_active"])

    @patch('controllers.db')
    def test_get_active_items_with_correct_format(self, mock_db):
        result = controllers.ItemController.get_active_items()

        self.assertIsInstance(result, unittest.mock.Mock)
        mock_db.SimpleDB.assert_called_once()
        mock_db.SimpleDB().query.assert_called_once_with("is_active", "YES")
