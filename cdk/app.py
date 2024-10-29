"""
This file is the entry point for the CDK application. It creates the stack and adds the resources to it.
"""

from aws_cdk import Stack
from aws_cdk import aws_cognito as cognito
from constructs import Construct


class TodosAppStack(Stack):

    def __init__(self, scope: Construct, stack_id: str, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        # The code that defines your stack goes here
        user_pool = cognito.UserPool(
            self,
            "UserPool",
            user_pool_name="TodosUserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(username=True, email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True),
                given_name=cognito.StandardAttribute(required=True),
                family_name=cognito.StandardAttribute(required=True),
            ),
        )

        user_pool.add_client(
            "UserPoolClient",
            auth_flows=cognito.AuthFlow(user_password=True),
            generate_secret=True,
        )
