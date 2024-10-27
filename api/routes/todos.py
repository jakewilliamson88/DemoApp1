from fastapi import APIRouter

from api.models.definitions import TodoItem
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
    logger.info(user)
    return [
        TodoItem(
            todo_id=0,
            title="Finish this route",
            description="Stub response",
            completed=False,
        )
    ]


@router.get("/{todo_id}")
def get_todo(todo_id: int) -> TodoItem:
    return TodoItem(
        todo_id=todo_id,
        title="Finish this route",
        description="Stub response",
        completed=False,
    )


@router.post("/")
def create_todo() -> None:
    return


@router.patch("/{todo_id}")
def update_todo(todo_id: int) -> TodoItem:
    return TodoItem(
        todo_id=todo_id,
        title="Finish this route",
        description="Stub response",
        completed=False,
    )


@router.delete("/{todo_id}")
def delete_todo(todo_id: int) -> None:
    logger.info(todo_id)
    return
