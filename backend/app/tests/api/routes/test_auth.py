import random

from starlette.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models.users import UserUpload
from app.tests.utils.users import create_test_user


def test_login_create_user_and_login_return_code_200(db: Session, client: TestClient, user: UserUpload) -> None:
    test_user_dict = dict(user)
    test_user_dict["username"] = "username_" + str(random.randint(5,15))
    test_user = UserUpload(**test_user_dict)
    create_test_user(db=db, user=test_user)
    data_credentials = {"username": test_user.username, "password": test_user.plain_password}

    r = client.post(url=f"{settings.API_V1_STR}/auth/login/", data=data_credentials)
    response: dict = r.json()
    assert r.status_code == 200
    assert response.get("access_token") is not None