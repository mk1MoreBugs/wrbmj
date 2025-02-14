from starlette.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.users import get_auth_header, get_unique_username


def test_user_info_create_user_and_get_auth_header_return_username(db: Session, client: TestClient, unique_usernames: str) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    response = client.get(
        url=f"{settings.API_V1_STR}/users/me",
        headers=get_auth_header(db=db, client=client, username=username, plain_password="plain_password")
    )
    assert response.status_code == 200
    assert response.json().get("username") == username


