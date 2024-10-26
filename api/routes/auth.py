"""
This file contains the auth routes for the application.
"""

from fastapi import APIRouter, HTTPException

from api.constants import USER_POOL_ID
from api.models.definitions import AuthRequest
from api.utils import get_sessioned_boto3, init_logger

router = APIRouter(
    prefix="/auth",
)

# Get a logger for the application.
logger = init_logger()

# Get Boto3 w/ a session.
boto3 = get_sessioned_boto3()


@router.post("/register")
def register(body: AuthRequest):
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

    logger.info(f"User {body.email} registered successfully")


@router.post("/login")
def login(body: AuthRequest):
    return
