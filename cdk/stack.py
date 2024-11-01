"""
This file contains the App Stack definition.
"""

import os

import constants
from aws_cdk import Duration, RemovalPolicy, Stack, aws_apigateway
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from constructs import Construct


class TodosAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the User Pool.
        user_pool = cognito.UserPool(
            self,
            constants.USER_POOL_NAME,
            user_pool_name=constants.USER_POOL_NAME,
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=False),
            auto_verify=cognito.AutoVerifiedAttrs(email=False),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True),
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_digits=True,
                require_lowercase=True,
                require_uppercase=True,
                require_symbols=True,
            ),
            removal_policy=RemovalPolicy.DESTROY,  # Dangerous!!! - only using because this is a demo
        )

        # Define the User Pool Client.
        user_pool.add_client(
            constants.USER_POOL_CLIENT_NAME,
            auth_flows=cognito.AuthFlow(user_password=True),
            generate_secret=False,
        )

        # Define the Todos Table.
        dynamodb.Table(
            self,
            constants.TODO_TABLE_NAME,
            table_name=constants.TODO_TABLE_NAME,
            partition_key=dynamodb.Attribute(
                name="owner_id",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="created_at",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            table_class=dynamodb.TableClass.STANDARD,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Create the Lambda function for the Todos API.
        dockerfile_path = os.path.join(os.path.dirname(__file__), "..")
        handler = lambda_.DockerImageFunction(
            self,
            constants.API_LAMBDA_NAME,
            code=lambda_.DockerImageCode.from_image_asset(dockerfile_path),
            timeout=Duration.seconds(constants.LAMBDA_TIMEOUT),
            logging_format=lambda_.LoggingFormat.JSON,
            application_log_level_v2=lambda_.ApplicationLogLevel.INFO,
        )

        # Let Lambda talk to Cognito and DynamoDB.
        # TODO: This is too permissive. Lock down the permissions.
        handler.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "cognito-idp:GetUser",
                    "cognito-idp:AdminCreateUser",
                    "cognito-idp:AdminSetUserPassword",
                    "cognito-idp:ListUserPools",
                    "cognito-idp:ListUserPoolClients",
                    "cognito-idp:InitiateAuth",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:DeleteItem",
                    "dynamodb:Query",
                ],
                resources=["*"],
            )
        )

        # Create the API Gateway.
        api = aws_apigateway.RestApi(
            self,
            constants.API_NAME,
            deploy=True,
            rest_api_name=constants.API_NAME,
            description="Demo API Gateway for Todos App",
        )

        # Add the Lambda integration to the API Gateway.
        resource = api.root.resource_for_path("v1/{proxy+}")
        resource.add_method(
            "ANY",
            aws_apigateway.LambdaIntegration(handler),
            authorization_type=aws_apigateway.AuthorizationType.NONE,
        )
