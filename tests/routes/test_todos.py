"""
This file contains the tests for the todos routes.
"""

from unittest import TestCase
from unittest.mock import patch

from api.models.definitions import TodoItem
from api.routes.auth import get_user
from main import app
from tests.utils import dependency_override_get_user, get_client


class TestTodos(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTodos, self).__init__(*args, **kwargs)
        self.client = get_client()

    @staticmethod
    def _override_get_user_dependency():
        """
        Override the `get_user` dependency for testing.
        :return:
        """

        app.dependency_overrides[get_user] = dependency_override_get_user

    @patch("api.routes.todos.TodoItem")
    def test_get_todos(self, mock_todo_item):
        """
        Test the `get_todos` function.
        :return:
        """

        # Test the route w/o authorization.
        todos = self.client.get("/todos")
        assert todos.status_code == 401

        # Override the `get_user` dependency.
        self._override_get_user_dependency()

        # Mock the response.
        mock_todo_item.get.return_value = TodoItem(
            owner_id="-1",
            created_at="1900-01-01",
            title="Test",
            description="Test",
        )

        todos = self.client.get("/todos/1900-01-01")
        assert todos.status_code == 200
