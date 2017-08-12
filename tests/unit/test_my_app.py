import unittest
from unittest.mock import patch

from my_app import app


class AppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index_view_should_return_hello_world(self):
        response = self.app.get("/")
        self.assertIn(b"hello world", response.data)

    def test_add_form_view_should_use_correct_template(self):
        response = self.app.get("/add-form")
        self.assertIn(b"Add item form", response.data)

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
        self.assertIn(b"great success!", response.data)

    @patch('my_app.controllers')
    def test_add_post_view_should_return_failed_message(self, mock_module):
        response = self.app.post("/add-post", data={})
        self.assertIn(b"failed", response.data)
