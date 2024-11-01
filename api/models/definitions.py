from datetime import datetime

import pytz
from dyntastic import Dyntastic
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.models.types import NonEmptyString
from cdk.constants import TODO_TABLE_NAME


class User(BaseModel):

    # Configure model to allow population by field name
    # and convert all string fields (username, email) to lowercase
    model_config = ConfigDict(
        populate_by_name=True,
        str_to_lower=True,
    )

    email: str = Field(
        ...,
        title="The email of the user",
        description="The email of the user",
    )


class TodoItem(Dyntastic):

    # Table settings.
    __table_name__ = TODO_TABLE_NAME
    __hash_key__ = "owner_id"
    __range_key__ = "created_at"

    # Allow the model to be populated by field name.
    model_config = ConfigDict(
        populate_by_name=True,
    )

    created_at: str = Field(
        default_factory=lambda: datetime.now(tz=pytz.UTC).isoformat(),
        title="Timestamp of when the todo was created",
        description="Timestamp of when the todo was created",
    )
    owner_id: str = Field(
        ...,
        title="The email of the user who owns the todo item",
        description="The email of the user who owns the todo item",
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


class TodoItemRequest(BaseModel):
    title: NonEmptyString = Field(
        ...,
        max_length=80,
        title="The title of the todo item",
        examples=["Buy groceries", "Walk the dog"],
    )
    description: NonEmptyString = Field(
        ...,
        max_length=500,
        title="The description of the todo item",
    )
    completed: bool | None = Field(
        default=False, description="Whether the todo item is completed or not"
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
