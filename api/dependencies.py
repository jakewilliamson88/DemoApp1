"""
This file contains the dependencies used throughout the application.
"""

from typing import Annotated

from fastapi import Depends

from api.routes.auth import get_user

AuthDependency = Annotated[get_user, Depends(get_user)]
