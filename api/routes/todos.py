from fastapi import APIRouter

from api.models.definitions import TodoItem

router = APIRouter(
    prefix="/todos",
)


@router.get("/")
def get_todos() -> list[TodoItem]:
    return [
        TodoItem(
            todo_id=0,
            title="Finish this route",
            description="Stub response",
            completed=False,
        )
    ]


@router.get("/{todo_id}")
def get_todo(todo_id: TodoItem.todo_id) -> TodoItem:
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
def update_todo(todo_id: TodoItem.todo_id) -> TodoItem:
    return TodoItem(
        todo_id=todo_id,
        title="Finish this route",
        description="Stub response",
        completed=False,
    )


@router.delete("/{todo_id}")
def delete_todo(todo_id: TodoItem.todo_id) -> None:
    return
