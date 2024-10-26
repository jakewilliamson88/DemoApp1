from fastapi import APIRouter

router = APIRouter(
    prefix="/todos",
)


@router.get("/")
def get_todos():
    return {"message": "TODO"}


@router.get("/{todo_id}")
def get_todo(todo_id: int):
    return {"message": "TODO"}


@router.post("/")
def create_todo():
    return {"message": "TODO"}


@router.patch("/{todo_id}")
def update_todo():
    return {"message": "TODO"}
