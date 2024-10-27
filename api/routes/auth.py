"""
This file contains the auth routes for the application.
"""

from fastapi import APIRouter, HTTPException

from api.constants import USER_POOL_ID
from api.models.definitions import AccessToken, AuthRequest
from api.utils import get_sessioned_boto3, init_logger

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# Get a logger for the application.
logger = init_logger()

# Get Boto3 w/ a session.
boto3 = get_sessioned_boto3()


def auth_user(username, password):
    pass


@router.post("/register")
def register(body: AuthRequest):
    """
    Register a new user in the Cognito User Pool.
    Use AdminSetPassword to set the password as permanent
    so the user does not have to change it on first login.
    :param body:
    :return:
    """
    logger.info("Registering new user")

    # Get a cognito client.
    client = boto3.client("cognito-idp")

    # Register the user in Cognito.
    try:
        response = client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=body.email,
            TemporaryPassword=body.password,
            MessageAction="SUPPRESS",
        )
        logger.info(response)
    except client.exceptions.UsernameExistsException:
        logger.error(f"User {body.email} already exists")
        raise HTTPException(status_code=400, detail="User already exists.")

    # Set the password as permanent so the user does not have
    # to change it on first login.
    try:
        logger.info("Setting user password as permanent")
        client.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=body.email,
            Password=body.password,
            Permanent=True,
        )
    except client.exceptions.UserNotFoundException:

        # This should *never* happen.
        logger.error(f"User {body.email} not found")
        raise HTTPException(status_code=404, detail="User not found.")

    logger.info(f"User {body.email} registered successfully")


@router.post("/login", response_model=AccessToken)
def login(body: AuthRequest) -> AccessToken:

    # Get a cognito client.
    cognito_client = boto3.client("cognito-idp")

    # Get the User Pool Client from the User Pool ID.
    user_pool_clients = cognito_client.list_user_pool_clients(UserPoolId=USER_POOL_ID)
    user_pool_client = None
    for upc in user_pool_clients["UserPoolClients"]:
        if upc["UserPoolId"] == USER_POOL_ID:
            user_pool_client = upc
            break

    # If the client is not found, raise an error.
    if user_pool_client is None:
        logger.error(f"User Pool Client not found for User Pool ID {USER_POOL_ID}")
        raise HTTPException(status_code=500, detail="User Pool Client not found")

    # Get the User Pool Client ID.
    user_pool_client_id = user_pool_client["ClientId"]

    # Initiate the authentication flow.
    try:
        response = cognito_client.initiate_auth(
            ClientId=user_pool_client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": body.email,
                "PASSWORD": body.password,
            },
        )
        logger.info(response)
    except cognito_client.exceptions.UserNotFoundException:
        logger.error(f"User {body.email} not authorized")
        raise HTTPException(status_code=401, detail="User not authorized.")

    logger.info(f"User {body.email} logged in successfully")

    # Return the access token.
    access_token = response["AuthenticationResult"]["AccessToken"]
    return AccessToken(token=access_token)
