"""
This file contains the auth routes for the application.
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
)


@router.post("/register")
def register(body):
    return


@router.post("/login")
def login(body):
    return
