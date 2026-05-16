from starlette.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.users import get_auth_header, get_unique_username, create_test_user


def test_user_info_create_user_and_get_auth_header_return_username(db: Session, client: TestClient, unique_usernames: str) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    password = "plain_password"
    create_test_user(db=db, username=username, plain_password=password)

    response = client.get(
        url=f"{settings.API_V1_STR}/users/me",
        headers=get_auth_header(client=client, username=username, plain_password=password)
    )
    assert response.status_code == 200
    assert response.json().get("username") == username


def test_user_info_do_request_without_auth_header_return_exception(db: Session, client: TestClient, unique_usernames: str) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    password = "plain_password"
    create_test_user(db=db, username=username, plain_password=password)

    response = client.get(
        url=f"{settings.API_V1_STR}/users/me",
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated" # "Could not validate credentials"


def test_user_info_do_request_with_incorrect_auth_token_return_exception(db: Session, client: TestClient, unique_usernames: str) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    password = "plain_password"
    create_test_user(db=db, username=username, plain_password=password)

    response = client.get(
        url=f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": "Bearer "},
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "Could not validate credentials"


def test_create_user_create_return_created_status(db: Session, client: TestClient, unique_usernames: str) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    password = "plain_password"
    request_data = {
        "username": username,
        "plain_password": password,
        "photo_file": "c3RyaW5n",  # In the future, use the base64 encode when sending the object
    }

    response = client.post(
        url=f"{settings.API_V1_STR}/users/create",
        json=request_data
    )
    assert response.status_code == 201
    assert response.json().get("status") == "created"


def test_create_user_create_non_unique_user_return_exception(db: Session, client: TestClient, unique_usernames: str) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    password = "plain_password"
    create_test_user(db=db, username=username, plain_password=password)
    request_data = {
        "username": username,
        "plain_password": password,
        "photo_file": "c3RyaW5n",  # In the future, use the base64 encode when sending the object
    }

    response = client.post(
        url=f"{settings.API_V1_STR}/users/create",
        json=request_data
    )
    assert response.status_code == 409
    assert response.json().get("detail") == "username already exists"
