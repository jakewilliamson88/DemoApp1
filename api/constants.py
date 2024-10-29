"""
This file contains the constants used throughout the application.
"""

# The default AWS region.
DEFAULT_REGION = "us-east-1"

#: The Name of this app. This is used to generate names
#: for AWS resources like DynamoDB tables and Cognito User Pools.
APP_NAME = "DemoApp1"

#: The name of the User Pool.
USER_POOL_NAME = f"{APP_NAME}UserPool"

#: The name of the User Pool Client.
USER_POOL_CLIENT_NAME = f"{APP_NAME}UserPoolClient"

# DynamoDB Table for Users.
USER_TABLE_NAME = f"{APP_NAME}Users"

# DynamoDB Table for Todos.
TODO_TABLE_NAME = f"{APP_NAME}Todos"
