"""
This file contains the constants used throughout the application.
"""

# The default AWS region.
DEFAULT_REGION = "us-east-1"

# Cognito User Pool
USER_POOL_ID = "us-east-1_9qc3NdPAQ"

#: The Name of this app. This is used to generate names
#: for AWS resources like DynamoDB tables and Cognito User Pools.
APP_NAME = "DemoApp1"

# DynamoDB Table for Users.
USER_TABLE_NAME = f"{APP_NAME}Users"

# DynamoDB Table for Todos.
TODO_TABLE_NAME = f"{APP_NAME}Todos"
