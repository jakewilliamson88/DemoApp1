"""
This file contain util functions for the tests.
"""

from fastapi.testclient import TestClient

from api.models.definitions import User
from main import app


def get_client():
    """
    Get the test client for the application.
    :return:
    """

    return TestClient(app)


def dependency_override_get_user():
    """
    Override the `get_user` dependency for testing.
    :return:
    """

    return User(
        email="foo@bar.com",
        password="password",
        user_id="-1",
    )
