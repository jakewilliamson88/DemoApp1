"""
This file contains the callback route for the OAuth2.0 flow.
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
)


@router.get("/")
def get_auth():
    return "OK"
