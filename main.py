from fastapi import FastAPI
from mangum import Mangum

from api.routes.auth import router as auth_router
from api.routes.todos import router as todos_router

# Create the app
app = FastAPI()

# Create the handler for AWS Lambda.
handler = Mangum(app)

# Add routers.
app.include_router(auth_router)
app.include_router(todos_router)
