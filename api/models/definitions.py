from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.models.types import NonEmptyString


class User(BaseModel):
    # Configure model to allow population by field name
    # and convert all string fields (username, email) to lowercase
    model_config = ConfigDict(
        populate_by_name=True,
        str_to_lower=True,
    )

    user_id: int = Field(
        ...,
        alias="id",
    )
    username: NonEmptyString = Field(
        ...,
        max_length=50,
        title="The username of the user",
        description="The username of the user",
    )
    email: EmailStr = Field(
        ...,
        title="The email of the user",
        description="The email of the user",
    )


class TodoItem(BaseModel):
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
    )
    password: NonEmptyString = Field(
        ...,
        max_length=50,
        title="Password",
        description="The user's password",
    )
