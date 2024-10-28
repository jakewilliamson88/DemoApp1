"""
This file contains the tests for the todos routes.
"""

from unittest import TestCase
from unittest.mock import Mock, patch

from dyntastic.exceptions import DoesNotExist

from api.models.definitions import TodoItem
from api.routes.auth import get_user
from main import app
from tests.utils import dependency_override_get_user, get_client


class TestTodos(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTodos, self).__init__(*args, **kwargs)

    @staticmethod
    def _override_get_user_dependency():
        """
        Override the `get_user` dependency for testing.
        :return:
        """

        app.dependency_overrides[get_user] = dependency_override_get_user

    @staticmethod
    def _reset_user_dependency():
        """
        Reset the `get_user` dependency.
        :return:
        """

        app.dependency_overrides[get_user] = get_user

    @patch("api.routes.todos.TodoItem")
    def test_get_todos(self, mock_todo_item):
        """
        Test the `get_todos` function.
        :return:
        """

        # Create a test client.
        client = get_client()

        # Test the route w/o authorization.
        todos = client.get("/todos")
        self.assertEqual(todos.status_code, 401)

        # Override the `get_user` dependency.
        self._override_get_user_dependency()

        # Mock the response.
        mock_todo_item.get.return_value = Mock()

        todos = client.get("/todos")
        assert todos.status_code == 200

        # Reset
        self._reset_user_dependency()

    @patch("api.routes.todos.TodoItem")
    def test_get_todo(self, mock_todo_item):

        # Create a test client.
        client = get_client()

        # Test the route w/o authorization.
        todo = client.get("/todos/1900-01-01")
        self.assertEqual(todo.status_code, 401)

        # Override the `get_user` dependency.
        self._override_get_user_dependency()

        # Mock a response to induce a 404.
        mock_todo_item.get.side_effect = DoesNotExist

        # # Test the route w/ authorization - Item not found.
        todo = client.get("/todos/1900-01-01")
        self.assertEqual(todo.status_code, 404)
        self.assertEqual(todo.json(), {"detail": "Todo not found."})

        # Remove side effect.
        mock_todo_item.get.side_effect = None

        # Mock the response.
        mock_todo_item.get.return_value = TodoItem(
            owner_id="-1",
            created_at="1900-01-01",
            title="Test Title",
            description="Test Description",
        )

        # Test the route w/ authorization - Item found.
        todo = client.get("/todos/1900-01-01")
        self.assertEqual(todo.status_code, 200)

        # Reset
        self._reset_user_dependency()

    @patch("api.routes.todos.TodoItem")
    def test_create_todo(self, mock_todo_item):
        """
        Test creating a new TodoItem
        :param mock_todo_item:
        :return:
        """

        # Create a test client.
        client = get_client()

        # Test the route w/o authorization.
        todo = client.post("/todos")
        self.assertEqual(todo.status_code, 401)

        # Override the `get_user` dependency.
        self._override_get_user_dependency()

        # Mock the response.
        mock_todo_item.save.return_value = Mock()

        # Create an item request.
        item_request = {
            "title": "Test Title",
            "description": "Test Description",
        }

        # Test the route w/ authorization.
        todo = client.post("/todos", json=item_request)
        self.assertEqual(todo.status_code, 200)

        # Reset
        self._reset_user_dependency()

    @patch("api.routes.todos.TodoItem")
    def test_update_todo(self, mock_todo_item):
        """
        Test updating a TodoItem.
        :param mock_todo_item:
        :return:
        """

        # Create a test client.
        client = get_client()

        # Test the route w/o authorization.
        todo = client.put("/todos/1900-01-01")
        self.assertEqual(todo.status_code, 401)

        # Override the `get_user` dependency.
        self._override_get_user_dependency()

        # Create an item request.
        item_request = {
            "title": "UPDATED",
            "description": "UPDATED",
        }

        # Set the side effect to induce a 404.
        mock_todo_item.get.side_effect = DoesNotExist

        # Test the route w/ authorization - Item not found.
        todo = client.put("/todos/1900-01-01", json=item_request)
        self.assertEqual(todo.status_code, 404)
        self.assertEqual(todo.json(), {"detail": "Todo not found."})

        # Mock the response.
        mock_todo_item.get.return_value = TodoItem(
            owner_id="-1",
            created_at="1900-01-01",
            title="NOT UPDATED",
            description="NOT UPDATED",
        )

        # Remove the side effect.
        mock_todo_item.get.side_effect = None

        # Test the route w/ authorization - Item found.
        todo = client.put("/todos/1900-01-01", json=item_request)
        self.assertEqual(todo.status_code, 200)

        # Assert updates.
        todo_response = todo.json()
        self.assertEqual(todo_response["title"], item_request["title"])
        self.assertEqual(todo_response["description"], item_request["description"])

        # Reset
        self._reset_user_dependency()

    @patch("api.routes.todos.TodoItem")
    def test_delete_todo(self, mock_todo_item):
        """
        Test deleting a TodoItem.
        :param mock_todo_item:
        :return:
        """

        # Create a test client.
        client = get_client()

        # Test the route w/o authorization.
        todo = client.delete("/todos/1900-01-01")
        self.assertEqual(todo.status_code, 401)

        # Override the `get_user` dependency.
        self._override_get_user_dependency()

        # Set the side effect to induce a 404.
        mock_todo_item.get.side_effect = DoesNotExist

        # Test the route w/ authorization - Item not found.
        todo = client.delete("/todos/1900-01-01")
        self.assertEqual(todo.status_code, 404)
        self.assertEqual(todo.json(), {"detail": "Todo not found."})

        # Mock the response.
        mock_todo_item.get.return_value = TodoItem(
            owner_id="-1",
            created_at="1900-01-01",
            title="Test Title",
            description="Test Description",
        )

        # Remove the side effect.
        mock_todo_item.get.side_effect = None

        # Test the route w/ authorization - Item found.
        todo = client.delete("/todos/1900-01-01")
        self.assertEqual(todo.status_code, 200)

        # Reset
        self._reset_user_dependency()
