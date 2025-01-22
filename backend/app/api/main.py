from fastapi import APIRouter


api_router = APIRouter(
    tags = ["hello world"],
)


@api_router.get("/")
def hello_world():
    return "hello FastAPI!"
