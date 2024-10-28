"""
This file contain util functions for the tests.
"""

from fastapi.testclient import TestClient

from main import app


def get_client():
    """
    Get the test client for the application.
    :return:
    """

    return TestClient(app)
