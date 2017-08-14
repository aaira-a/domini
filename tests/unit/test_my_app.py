import unittest
from unittest.mock import Mock, patch

from my_app import app, scheduled


class AppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index_view_should_return_hello_world(self):
        response = self.app.get("/")
        self.assertIn(b"hello world", response.data.lower())

    def test_add_form_view_should_use_correct_template(self):
        response = self.app.get("/add-form")
        self.assertIn(b"track an order", response.data.lower())

    @patch('my_app.controllers')
    def test_add_post_view_should_call_model_controller(self, mock_module):
        data = {"url": "myurl1", "phone": "+60123", "token": "mytoken1"}

        self.app.post("/add-post", data=data)

        mock_module.ItemController.assert_called()
        mock_module.ItemController().add.assert_called_with(
            "myurl1", "mytoken1", "+60123")

    @patch('my_app.controllers')
    def test_add_post_view_should_return_success_message(self, mock_module):
        data = {"url": "myurl1", "phone": "+60123", "token": "mytoken1"}
        response = self.app.post("/add-post", data=data)
        self.assertIn(b"great success!", response.data.lower())

    @patch('my_app.controllers')
    def test_add_post_view_should_return_failed_message(self, mock_module):
        response = self.app.post("/add-post", data={})
        self.assertIn(b"failed", response.data.lower())


@patch('my_app.controllers')
class ScheduledFunctionTests(unittest.TestCase):

    def test_scheduled_should_return_scheduled_string(self, _):
        self.assertIn("schedule triggered on", scheduled())

    def test_scheduled_should_call_model_controller(self, mock_module):
        mock_items = []
        mock_controller_instance = Mock()
        mock_controller_instance.get_active_items.return_value = []
        mock_module.ItemController.return_value = mock_controller_instance

        scheduled()

        mock_module.ItemController.assert_called_once()
        mock_controller_instance.get_active_items.assert_called_once()
        mock_controller_instance.process_items.assert_called_once_with(mock_items)
