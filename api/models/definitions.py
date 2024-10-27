from uuid import uuid4

from dyntastic import Dyntastic
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.constants import TODO_TABLE_NAME, USER_TABLE_NAME
from api.models.types import NonEmptyString


class User(Dyntastic):

    # Table settings.
    __table_name__ = USER_TABLE_NAME
    __hash_key__ = "email"

    # Configure model to allow population by field name
    # and convert all string fields (username, email) to lowercase
    model_config = ConfigDict(
        populate_by_name=True,
        str_to_lower=True,
    )

    user_id: int = Field(
        ...,
        default_factory=lambda: uuid4().int,
        alias="id",
        title="The id of the user",
        description="The id of the user",
    )

    email: EmailStr = Field(
        ...,
        title="The email of the user",
        description="The email of the user",
    )


class TodoItem(BaseModel):

    # Table settings.
    __table_name__ = TODO_TABLE_NAME
    __hash_key__ = "todo_id"

    # Allow the model to be populated by field name.
    model_config = ConfigDict(
        populate_by_name=True,
    )

    todo_id: int = Field(
        ...,
        alias="id",
        title="The id of the todo item",
        description="The id of the todo item",
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=80,
        title="The title of the todo item",
        examples=["Buy groceries", "Walk the dog"],
    )
    description: NonEmptyString = Field(
        ...,
        max_length=500,
        description="The description of the todo item",
    )
    completed: bool = Field(
        False, description="Whether the todo item is completed or not"
    )


class AuthRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        max_length=50,
        title="Email Address",
        description="The user's email address",
        examples=["foo@bar.com"],
    )
    password: NonEmptyString = Field(
        ...,
        max_length=50,
        title="Password",
        description="The user's password",
        examples=["ABCabc123!@#"],
    )


class AccessToken(BaseModel):
    access_token: str = Field(
        ...,
        title="Token",
        description="The user's access token",
    )
    token_type: str = "Bearer"
