from sqlmodel import Session
from starlette.testclient import TestClient
from httpx import Response

from app.core.config import settings
from app.core.security import get_password_hash
from app.crud import users
from app.models import UserInDb


def create_test_user(db: Session, username: str, plain_password: str):
    users_for_write_db = UserInDb(
        username=username,
        hashed_password=get_password_hash(password=plain_password),
        photo_file_name="path/to/file"
    )
    users.create_user(session=db, user=users_for_write_db)


def get_unique_username(unique_usernames) -> str:
    unique_username_count = len(unique_usernames)
    unique_username = "username_" + str(unique_username_count)
    unique_usernames.add(unique_username)
    return unique_username


def get_auth_token_response(
        client: TestClient,
        username: str,
        plain_password: str
) -> Response:
    data_credentials = {"username": username, "password": plain_password}

    return client.post(url=f"{settings.API_V1_STR}/auth/login/", data=data_credentials)


def get_auth_header(
        client: TestClient,
        username: str,
        plain_password: str
) -> dict[str, str]:
    response = get_auth_token_response(
        client=client,
        username=username,
        plain_password=plain_password
    )
    auth_token: dict[str, str] = response.json()
    return {"Authorization": "Bearer " + auth_token["access_token"]}
