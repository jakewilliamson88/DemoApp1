"""
This file contain util functions for the tests.
"""

from fastapi.testclient import TestClient

from main import app

# Set up the test client.
client = TestClient(app)
