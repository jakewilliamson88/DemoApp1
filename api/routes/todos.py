from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, HTTPException

from api.models.definitions import TodoItem, TodoItemRequest
from api.routes.auth import AuthDependency
from api.utils import init_logger

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
)

# Get a logger for the application.
logger = init_logger()


@router.get("/")
def get_todos(user: AuthDependency) -> list[TodoItem]:
    """
    Fetch Todos for the User from Dynamo.
    :param user:
    :return:
    """

    logger.info(f"Fetching Todos for {user.email}")

    # Get the User's Todos from Dynamo.
    try:
        todos = TodoItem.query(user.email)
        return [todo for todo in todos]
    except DoesNotExist:
        logger.info(f"User {user.email} does not have any Todos yet")
        return []


@router.get("/{created_at}")
def get_todo(user: AuthDependency, created_at: str) -> TodoItem:
    """
    Fetch a specific TodoItem for the User from Dynamo.
    :param user:
    :param created_at:
    :return:
    """

    try:
        return TodoItem.get(user.email, created_at)
    except DoesNotExist:
        logger.info(f"Todo {created_at} not found")
        raise HTTPException(status_code=404, detail="Todo not found.")


@router.post("/")
def create_todo(user: AuthDependency, request: TodoItemRequest) -> None:
    """
    Create a new TodoItem for the User in Dynamo.
    :param user:
    :param request:
    :return:
    """

    try:
        todo = TodoItem(
            owner_id=user.email,
            title=request.title,
            description=request.description,
            completed=False,
        )

        todo.save()
    except Exception as e:
        logger.error(f"Failed to create Todo for {user.email}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Failed to create Todo.")


@router.put("/{created_at}")
def update_todo(
    user: AuthDependency, created_at: str, request: TodoItemRequest
) -> TodoItem:
    """
    Update a TodoItem for the User in Dynamo.
    :param user:
    :param created_at:
    :param request:
    :return:
    """

    # Get the TodoItem from Dynamo.
    try:
        todo = TodoItem.get(user.email, created_at)
    except DoesNotExist:
        logger.info(f"Todo {created_at} not found")
        raise HTTPException(status_code=404, detail="Todo not found.")

    # Update the TodoItem.
    todo.title = request.title
    todo.description = request.description
    todo.completed = request.completed
    todo.save()

    return todo


@router.delete("/{created_at}")
def delete_todo(user: AuthDependency, created_at: str) -> None:
    """
    Delete a TodoItem for the User from Dynamo.
    :param user:
    :param created_at:
    :return:
    """

    # Get the TodoItem from Dynamo.
    try:
        todo = TodoItem.get(user.email, created_at)
    except DoesNotExist:
        logger.info(f"Todo {created_at} not found")
        raise HTTPException(status_code=404, detail="Todo not found.")

    # Delete the TodoItem.
    todo.delete()
