"""
This file contains the App Stack definition.
"""

from aws_cdk import RemovalPolicy, Stack
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_dynamodb as dynamodb
from constants import APP_NAME
from constructs import Construct


class TodosAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the User Pool.
        user_pool = cognito.UserPool(
            self,
            f"{APP_NAME}UserPool",
            user_pool_name=f"{APP_NAME}UserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(username=True, email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True),
                given_name=cognito.StandardAttribute(required=True),
                family_name=cognito.StandardAttribute(required=True),
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_digits=True,
                require_lowercase=True,
                require_uppercase=True,
                require_symbols=True,
            ),
        )

        # Define the User Pool Client.
        user_pool.add_client(
            f"{APP_NAME}UserPoolClient",
            auth_flows=cognito.AuthFlow(user_password=True),
            generate_secret=True,
        )

        # Define the Todos Table.
        dynamodb.Table(
            self,
            f"{APP_NAME}Todos",
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

        # Define the Users Table.
        dynamodb.Table(
            self,
            f"{APP_NAME}Users",
            partition_key=dynamodb.Attribute(
                name="email",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            table_class=dynamodb.TableClass.STANDARD,
            removal_policy=RemovalPolicy.DESTROY,
        )
