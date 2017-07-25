import unittest
from unittest.mock import patch

import controllers


class ItemControllerTests(unittest.TestCase):

    def setUp(self):
        self.mock_db_instance = unittest.mock.Mock()
        self.mock_db_module = unittest.mock.Mock()
        self.mock_db_module.SimpleDB.return_value = self.mock_db_instance

    def test_controller_init_should_instantiate_db(self):
        controller = controllers.ItemController(self.mock_db_module)

        self.mock_db_module.SimpleDB.assert_called_once()
        self.assertEqual(controller.db, self.mock_db_instance)

    @patch('controllers.Item')
    def test_add_item_saves_correct_fields_to_model(self, mock_Item):
        self.url = "https://abc/def/ghi?jkl=mno"
        self.token = "Bearer xyz"

        controller = controllers.ItemController(self.mock_db_module)
        controller.add(self.url, self.token)

        mock_Item.assert_called_with(self.url, self.token,
                                     self.mock_db_instance)
        mock_Item().save.assert_called_with(
            fields=["url", "token", "failed_count", "is_active"])

    def test_get_active_items_with_correct_format(self):
        expected = {"Items": [{"item1": "abc"}, {"item2": "def"}]}
        self.mock_db_instance.query.return_value = expected

        controller = controllers.ItemController(self.mock_db_module)
        results = controller.get_active_items()

        self.mock_db_instance.query.assert_called_once_with("is_active", "YES")
        self.assertEqual(expected, results)
