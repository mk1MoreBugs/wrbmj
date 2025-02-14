from starlette.testclient import TestClient
from sqlmodel import Session

from app.tests.utils.users import get_auth_token_response, get_unique_username, create_test_user


def test_login_create_user_and_login_return_code_200(db: Session, client: TestClient, unique_usernames: str) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    create_test_user(db=db, username=username, plain_password="plain_password")

    response = get_auth_token_response(
        client=client,
        username=username,
        plain_password="plain_password"
    )

    assert response.status_code == 200
    assert response.json().get("access_token") is not None