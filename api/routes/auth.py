"""
This file contains the auth routes for the application.
"""

from fastapi import APIRouter, Body

from api.utils import init_logger

router = APIRouter(
    prefix="/auth",
)

# Get a logger for the application.
logger = init_logger()


@router.post("/register")
def register(body):
    logger.info(body)
    return


@router.post("/login")
def login(body: Body()):
    return
