from fastapi import FastAPI
from mangum import Mangum

from api.routes.auth import router as auth_router
from api.routes.todos import router as todos_router

# Create the app
app = FastAPI(
    title="FastAPI - Demo App 1 - Todos API",
    version="0.0.1",
    root_path="/prod/v1",
    openapi_url="/openapi.json",
)

# Create the handler for AWS Lambda.
handler = Mangum(app, api_gateway_base_path="/v1")

# Add routers.
app.include_router(auth_router)
app.include_router(todos_router)
