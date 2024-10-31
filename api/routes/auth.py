"""
This file contains the auth routes for the application.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.models.definitions import AccessToken, AuthRequest, User
from api.utils import get_sessioned_boto3, get_user_pool_id, init_logger
from cdk.constants import USER_POOL_NAME

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# Get a logger for the application.
logger = init_logger()

# Get Boto3 w/ a session.
boto3 = get_sessioned_boto3()

# Dependency for login.
OAuth2Scheme = Annotated[OAuth2PasswordRequestForm, Depends()]

# Token dependency.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")
TokenDependency = Annotated[str, Depends(oauth2_bearer)]


def get_user(token: TokenDependency) -> User:
    """
    Get the user from the Cognito User Pool.
    :param token:
    :return:
    """

    # Get a cognito client.
    client = boto3.client("cognito-idp")

    # Get the user from the Cognito User Pool.
    try:
        response = client.get_user(AccessToken=token)
    except client.exceptions.NotAuthorizedException:
        logger.error("User not authorized")
        raise HTTPException(status_code=401, detail="User not authorized.")

    # Get the User model.
    return User(email=response["Username"])


# Dependency for route access.
AuthDependency = Annotated[User, Depends(get_user)]


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

    # Get the User Pool ID.
    user_pool_id = get_user_pool_id(USER_POOL_NAME)

    # Register the user in Cognito.
    try:
        client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=body.email,
            TemporaryPassword=body.password,
            MessageAction="SUPPRESS",
        )
    except client.exceptions.UsernameExistsException:
        logger.error(f"User {body.email} already exists")
        raise HTTPException(status_code=400, detail="User already exists.")

    # Set the password as permanent so the user does not have
    # to change it on first login.
    try:
        logger.info("Setting user password as permanent")
        client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=body.email,
            Password=body.password,
            Permanent=True,
        )
    except client.exceptions.UserNotFoundException:

        # This should *never* happen.
        logger.error(f"User {body.email} not found")
        raise HTTPException(status_code=404, detail="User not found.")

    logger.info(f"User {body.email} registered successfully in Cognito")

    # Prevent double-registration in Dynamo.
    existing_user = User.safe_get(body.email)
    if existing_user:
        logger.error(f"User {body.email} already exists in DynamoDB")
        raise HTTPException(status_code=400, detail="User already exists.")


@router.post("/login")
def login(body: OAuth2Scheme) -> dict:
    # Get a cognito client.
    cognito_client = boto3.client("cognito-idp")

    # Get the User Pool ID.
    user_pool_id = get_user_pool_id(USER_POOL_NAME)

    # Get the User Pool Client from the User Pool ID.
    user_pool_clients = cognito_client.list_user_pool_clients(UserPoolId=user_pool_id)
    user_pool_client = None
    for upc in user_pool_clients["UserPoolClients"]:
        if upc["UserPoolId"] == user_pool_id:
            user_pool_client = upc
            break

    # If the client is not found, raise an error.
    if user_pool_client is None:
        logger.error(f"User Pool Client not found for User Pool ID {user_pool_id}")
        raise HTTPException(status_code=500, detail="User Pool Client not found")

    # Get the User Pool Client ID.
    user_pool_client_id = user_pool_client["ClientId"]

    # Initiate the authentication flow.
    try:
        response = cognito_client.initiate_auth(
            ClientId=user_pool_client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": body.username,
                "PASSWORD": body.password,
            },
        )
    except cognito_client.exceptions.UserNotFoundException:
        logger.error(f"User {body.username} not authorized")
        raise HTTPException(status_code=401, detail="User not authorized.")
    except cognito_client.exceptions.NotAuthorizedException:
        logger.error(f"User {body.username} not authorized")
        raise HTTPException(status_code=401, detail="User not authorized.")

    logger.info(f"User {body.username} logged in successfully")

    # Return the access token.
    access_token = response["AuthenticationResult"]["AccessToken"]
    response = AccessToken(access_token=access_token)

    return response.model_dump()
