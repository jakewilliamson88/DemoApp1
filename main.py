from fastapi import FastAPI

from api.routes.auth import router as auth_router
from api.routes.todos import router as todos_router

# Create the app
app = FastAPI()

# Add routers.
app.include_router(auth_router)
app.include_router(todos_router)
