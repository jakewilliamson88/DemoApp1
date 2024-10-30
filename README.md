# Demo App 1 - Todos

This is a simple "TODO" API that allows users to create, read, update, and delete tasks.
it is complete with authentication and authorization.
You can create an account, log in, and create tasks that are only visible to you.

---

## Usage

Recommended python version: `3.12`

To run this project locally clone this repo, `cd` into the root directory and do the following:

If you haven't already, set up your AWS credentials.
This application uses boto3 which expects your AWS credentials to be in `~/.aws/credentials`.
You can automate this process by running `aws configure` and following the prompts.

The following commands will install the necessary dependencies, deploy the infrastructure to AWS, and run the FastAPI server.

```bash
# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install AWS CDK.
npm install -g aws-cdk

# View the services that will be deployed (optional).
cdk diff

# The first time you run this, you'll need to bootstrap the application.
cdk bootstrap

# Deploy infrastructure on AWS.
cdk deploy

# Run the FastAPI server
uvicorn main:app --reload
```

You will see output similar to the following:

```
INFO:     Will watch for changes in these directories: ['/path/to/DemoApp1']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [72950] using StatReload
INFO:     Started server process [72952]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Then point your browser to `http://127.0.0.1:8000/docs` to see the Swagger UI.

From there, you can create an account, log in, and create tasks.
Register a new user with the `POST /register/` endpoint.
Authenticate with the `Authorize` button near the top-right of the page.
This will authorize your requests to other endpoints with a JWT token.

To automatically tear down the infrastructure, run the following command:

```bash
cdk destroy
```


## Notes for Potential Employers / Recruiters

This app is for demonstration purposes only.
It is a project I've created to demonstrate different development principles and techniques.
If you're a potential employer or recruiter, please take note of the following:

1. - [X] Pydantic Data Modeling and Validation
2. - [X] Use of Dyntastic for DynamoDB integration
3. - [X] Sane git repository:
   * - [X] Proper commit messages
   * - [X] Proper branching
   * - [X] Proper documentation
   * - [X] Proper `.gitignore`
   * - [X] Proper branch protections
4. - [X] Use of GitHub Actions for CI/CD
   * - [X] Linting
   * - [X] Testing
   * - [X] Formatting
   * - [X] Deployment
5. - [X] Use of AWS Services:
   * - [X]  Cognito
   * - [X]  DynamoDB
   * - [X]  Lambda
   * - [X]  API Gateway
6. - [X] IaC via CDK:
   * - [X]  Cognito
   * - [X]  DynamoDB
   * - [X]  Lambda
   * - [X]  API Gateway
7. - [X] Docker
8. - [X] Documentation
