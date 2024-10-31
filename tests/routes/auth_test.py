"""
This file contains the tests for the auth routes.
"""

from unittest import TestCase
from unittest.mock import Mock, patch

from api.models.definitions import AuthRequest
from api.routes.auth import get_user
from tests.utils import get_client


class TestAuth(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestAuth, self).__init__(*args, **kwargs)
        self.client = get_client()

    @patch("api.routes.auth.boto3")
    def test_get_user(self, mock_boto3):
        """
        Test the `get_user` function.
        :return:
        """

        # Mock boto3 responses.
        mock_boto3.client.return_value = Mock(email="foo@bar.com")
        mock_boto3.client.return_value.get_user.return_value = {
            "Username": "foo@bar.com"
        }

        # Test the call.
        user = get_user("token")
        self.assertEqual(user.email, "foo@bar.com")

        # Check error path - User not found in Cognito.
        mock_boto3.client.return_value.get_user.side_effect = Exception
        with self.assertRaises(Exception):
            get_user("spam")

    @patch("api.routes.auth.get_user_pool_id")
    @patch("api.routes.auth.boto3")
    def test_register(self, mock_boto3, mock_get_user_pool_id):
        """
        Test the register route.
        """

        # Define the User Pool ID.
        mock_get_user_pool_id.return_value = "user_pool_id"

        # Mock boto3 responses.
        mock_boto3.client.return_value = Mock()

        # Define the request body.
        request = AuthRequest(email="foo@bar.com", password="password")

        # Make the request.
        response = self.client.post("/auth/register", json=request.model_dump())

        # Assert success response.
        self.assertEqual(response.status_code, 200)

        # TODO: Test exceptions.

    @patch("api.routes.auth.get_user_pool_id")
    @patch("api.routes.auth.boto3")
    def test_login(self, mock_boto3, mock_get_user_pool_id):
        """
        Test the login route.
        """

        # Define the User Pool ID.
        mock_get_user_pool_id.return_value = "user_pool_id"

        # Mock boto3 responses.
        mock_boto3.client.return_value = Mock()
        mock_boto3.client.return_value.list_user_pool_clients.return_value = {
            "UserPoolClients": [{"UserPoolId": "user_pool_id", "ClientId": "baz"}]
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
