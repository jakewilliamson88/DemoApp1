"""
This file contains the tests for the auth routes.
"""

from unittest import TestCase
from unittest.mock import Mock, patch

from api.constants import USER_POOL_ID
from api.models.definitions import AuthRequest
from tests.utils import get_client


class TestAuth(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestAuth, self).__init__(*args, **kwargs)
        self.client = get_client()

    @patch("api.routes.auth.boto3")
    @patch("api.routes.auth.User")
    def test_register(self, mock_user, mock_boto3):
        """
        Test the register route.
        """

        # Mock boto3 responses.
        mock_boto3.client.return_value = Mock()

        # Mock the User model.
        mock_user.safe_get.return_value = None
        mock_user.save.return_value = None

        # Define the request body.
        request = AuthRequest(email="foo@bar.com", password="password")

        # Make the request.
        response = self.client.post("/auth/register", json=request.model_dump())

        # Assert success response.
        self.assertEqual(response.status_code, 200)

        # TODO: Test exceptions.

    @patch("api.routes.auth.boto3")
    def test_login(self, mock_boto3):
        """
        Test the login route.
        """

        # Mock boto3 responses.
        mock_boto3.client.return_value = Mock()
        mock_boto3.client.return_value.list_user_pool_clients.return_value = {
            "UserPoolClients": [{"UserPoolId": USER_POOL_ID, "ClientId": "baz"}]
        }
        mock_boto3.client.return_value.initiate_auth.return_value = {
            "AuthenticationResult": {"AccessToken": "spam"}
        }

        # Define the request body.
        request = {
            "grant_type": "password",
            "username": "foo@bar.com",
            "password": "password",
            "scopes": [],
            "client_id": None,
            "client_secret": None,
        }

        # Make the request.
        # response = self.client.post("/auth/login", data=request)
        response = self.client.post("/auth/login", data=request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        # TODO: Test exceptions.
