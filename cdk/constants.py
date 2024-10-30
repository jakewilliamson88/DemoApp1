"""
This file contains the constants used throughout the CDK application.
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

# The ECR Repository name for the Docker container.
ECR_REPO_NAME = f"{APP_NAME}Repo"

# The Lambda function name for the Todos API.
API_LAMBDA_NAME = f"{APP_NAME}FastAPIHandler"

#: The name of the API Gateway.
API_NAME = f"{APP_NAME}Api"

#: The timeout for the Lambda function.
LAMBDA_TIMEOUT = 5
