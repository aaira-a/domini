import unittest
from unittest.mock import patch

import controllers

from query_result_fixture import results as mock_results


class ItemControllerTests(unittest.TestCase):

    def setUp(self):
        self.mock_db_instance = unittest.mock.MagicMock()
        self.mock_db_module = unittest.mock.Mock()
        self.mock_db_module.SimpleDB.return_value = self.mock_db_instance

        self.mock_messenger_instance = unittest.mock.MagicMock()
        self.mock_messenger_module = unittest.mock.Mock()
        self.mock_messenger_module.TwilioClient.return_value = self.mock_messenger_instance

        self.controller = controllers.ItemController(
            self.mock_db_module, self.mock_messenger_module)

    def test_controller_init_should_instantiate_db(self):
        self.mock_db_module.SimpleDB.assert_called_once()
        self.assertEqual(self.controller.db, self.mock_db_instance)
        self.mock_db_instance.create_domain.assert_called_once()

    def test_controller_init_should_instantiate_messenger(self):
        self.mock_messenger_module.TwilioClient.assert_called_once()
        self.assertEqual(self.controller.messenger,
                         self.mock_messenger_instance)

    @patch('controllers.Item')
    def test_add_item_saves_correct_fields_to_model(self, mock_Item):
        self.url = "https://abc/def/ghi?jkl=mno"
        self.token = "Bearer xyz"

        self.controller.add(self.url, self.token)

        mock_Item.assert_called_with(self.url, self.token,
                                     self.mock_db_instance)
        mock_Item().save.assert_called_with(
            fields=["url", "token", "phone", "failed_count", "is_active"])

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
            phone="+0123",
            failed_count=3,
            db=self.mock_db_instance)

        expected_object_2 = controllers.Item(
            is_existing=True,
            id_="9ac48b02-e125-4a4c-a67b-582cf87f9345",
            url="url3",
            token="token3",
            phone="+3210",
            failed_count=1,
            db=self.mock_db_instance)

        self.assertEqual(2, len(items))

        self.assertEqual(expected_object_1.id, items[0].id)
        self.assertEqual(expected_object_1.url, items[0].url)
        self.assertEqual(expected_object_1.token, items[0].token)
        self.assertEqual(expected_object_1.phone, items[0].phone)
        self.assertEqual(expected_object_1.failed_count, items[0].failed_count)

        self.assertEqual(expected_object_2.id, items[1].id)
        self.assertEqual(expected_object_2.url, items[1].url)
        self.assertEqual(expected_object_2.token, items[1].token)
        self.assertEqual(expected_object_2.phone, items[1].phone)
        self.assertEqual(expected_object_2.failed_count, items[1].failed_count)

    def test_process_items_calls_models_fetch_method(self):
        mock_item = unittest.mock.MagicMock()
        self.controller.process_items([mock_item])
        mock_item.fetch_status_from_provider.assert_called_once()

    def test_process_items_increments_failed_count_for_fetch_errors(self):
        mock_item = unittest.mock.MagicMock()
        mock_item.fetch_status_from_provider.return_value = "error"

        self.controller.process_items([mock_item])
        mock_item.increment_failed_count.assert_called_once()

    def test_process_items_do_not_send_message_if_status_is_error(self):
        mock_item = unittest.mock.MagicMock()
        mock_item.fetch_status_from_provider.return_value = "error"
        self.controller.process_items([mock_item])

        self.mock_messenger_instance.send_message.assert_not_called()

    def test_process_items_sends_message_if_status_is_DL(self):
        mock_item = unittest.mock.MagicMock()
        mock_item.fetch_status_from_provider.return_value = "DL"
        mock_item.phone = "+0123"

        self.controller.process_items([mock_item])

        self.mock_messenger_instance.send_message.assert_called_once_with(
            "your item is out for delivery now", mock_item.phone)

    def test_process_items_does_not_send_message_if_status_is_other(self):
        mock_item = unittest.mock.MagicMock()
        mock_item.fetch_status_from_provider.return_value = "randomstring"
        self.controller.process_items([mock_item])

        self.mock_messenger_instance.send_message.assert_not_called()

    def test_process_items_does_not_increment_failed_count_other_status(self):
        mock_item = unittest.mock.MagicMock()
        mock_item.fetch_status_from_provider.return_value = "randomstring"

        self.controller.process_items([mock_item])
        mock_item.increment_failed_count.assert_not_called()

    def test_process_items_sets_item_to_inactive_in_sending_msg_for_DL(self):
        mock_item = unittest.mock.MagicMock()
        mock_item.fetch_status_from_provider.return_value = "DL"
        mock_item.is_active = "YES"

        self.controller.process_items([mock_item])

        self.mock_messenger_instance.send_message.assert_called()
        self.assertEqual("NO", mock_item.is_active)

    def test_process_items_save_item_field_after_processing(self):
        mock_item = unittest.mock.MagicMock()
        self.controller.process_items([mock_item])
        mock_item.save.assert_called_with(
            fields=["url", "token", "phone", "failed_count", "is_active"])
