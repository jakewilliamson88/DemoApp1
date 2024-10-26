"""
This file contains the auth routes for the application.
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
)


@router.get("/")
def get_auth():
    return "OK"


@router.post("/login")
def login(body):
    return
