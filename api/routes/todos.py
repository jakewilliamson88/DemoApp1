from fastapi import APIRouter

router = APIRouter(
    prefix="/todos",
)


@router.get("/")
def get_todos():
    return {"message": "TODO"}
