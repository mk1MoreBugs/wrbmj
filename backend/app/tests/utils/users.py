import random

from sqlmodel import Session
from starlette.testclient import TestClient
from httpx import Response

from app.core.config import settings
from app.core.security import get_password_hash
from app.crud import users
from app.models import UserInDb
from app.models.users import UserUpload


def create_test_user(db: Session, user: UserUpload):
    users_for_write_db = UserInDb(
        **dict(user),
        hashed_password=get_password_hash(password=user.plain_password),
        photo_file_name="path/to/file"
    )
    users.create_user(session=db, user=users_for_write_db)


def get_auth_token_response(db: Session, client: TestClient, user: UserUpload) -> Response:
    test_user_dict = dict(user)
    test_user_dict["username"] = "username_" + str(random.randint(5, 15))
    test_user = UserUpload(**test_user_dict)
    create_test_user(db=db, user=test_user)
    data_credentials = {"username": test_user.username, "password": test_user.plain_password}

    return client.post(url=f"{settings.API_V1_STR}/auth/login/", data=data_credentials)


def get_auth_header(db: Session, client: TestClient, user: UserUpload) -> dict[str, str]:
    response = get_auth_token_response(db=db, client=client, user=user)
    auth_token: dict[str, str] = response.json()
    return {"Authorization": "Bearer " + auth_token["access_token"]}
