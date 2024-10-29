"""
This file contains the utility functions used throughout the application.
"""

import os

import boto3
from aws_lambda_powertools import Logger
from pydantic import BaseModel


def init_logger() -> Logger:
    """
    Initialize the logger for the application.
    """

    # Define the json default for Models.
    def json_default(value):
        if isinstance(value, BaseModel):
            return value.model_dump()
        return str(value)

    location_format = "%(module)s.%(funcName)s"
    logger = Logger(json_default=json_default)
    logger.append_keys(location=location_format)
    return logger


def get_sessioned_boto3():
    """
    Returns `boto3` with an initialized default Session.
    :return:
    """

    boto3.setup_default_session(profile_name=os.environ.get("AWS_PROFILE_NAME"))
    return boto3


def get_user_pool_id(user_pool_name: str) -> str:
    """
    Return the User Pool ID
    :return:
    """

    # Get a sessioned client.
    client = get_sessioned_boto3().client("cognito-idp")

    # Get the User Pool ID.
    pools = client.list_user_pools()
    for pool in pools["UserPools"]:
        if pool["Name"] == user_pool_name:
            return pool["Id"]
