"""
This file is the entry point for the CDK application. It creates the stack and adds the resources to it.
"""

import aws_cdk

from api.constants import DEFAULT_REGION
from cdk.stack import TodosAppStack

# Define the CDK App.
app = aws_cdk.App()

# Create the Stack.
stack = TodosAppStack(
    app, "TodosAppStack", env=aws_cdk.Environment(region=DEFAULT_REGION)
)

# Generate the CloudFormation template.
app.synth()
