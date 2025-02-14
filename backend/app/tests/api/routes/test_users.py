from starlette.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models.users import UserUpload
from app.tests.utils.users import get_auth_header


def test_user_info_create_user_and_get_auth_header_return_status_code_200(db: Session, client: TestClient, user: UserUpload) -> None:
    response = client.get(
        url=f"{settings.API_V1_STR}/users/me",
        headers=get_auth_header(db=db, client=client, user=user)
    )
    assert response.status_code == 200
    assert response.json().get("username") is not None