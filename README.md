# Demo App 1 - Todos

This is a simple "TODO" API that allows users to create, read, update, and delete tasks.
it is complete with authentication and authorization.
You can create an account, log in, and create tasks that are only visible to you.

---

## Usage

To run this project locally clone this repo, `cd` into the root directory and run the following commands:

```bash
# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload
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
Register a new user with the `POST /users/` endpoint.
Authenticate with the `Auuthorize` button near the top-right of the page.
This will authorize your requests to other endpoints with a JWT token.

TODO:
* Implement and document ability to fork the repo and auto-deploy this API to your AWS account

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
4. - [ ] Use of GitHub Actions for CI/CD
   * - [X] Linting
   * - [X] Testing
   * - [X] Formatting
   * - [ ] Deployment
5. - [ ] Use of AWS Services:
   * - [X]  Cognito
   * - [X]  DynamoDB
   * - [ ]  Lambda
   * - [ ]  API Gateway
   * - [ ]  ECR
   * - [ ]  ECS
6. - [ ] IaC via CDK:
   * - [ ]  Cognito
   * - [ ]  DynamoDB
   * - [ ]  Lambda
   * - [ ]  API Gateway
   * - [ ]  ECR
   * - [ ]  ECS
7. - [ ] Documentation
