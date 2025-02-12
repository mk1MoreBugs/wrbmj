from starlette.testclient import TestClient
from sqlmodel import Session

from app.models.users import UserUpload
from app.tests.utils.users import get_auth_token_response


def test_login_create_user_and_login_return_code_200(db: Session, client: TestClient, user: UserUpload) -> None:
    response = get_auth_token_response(db=db, client=client, user=user)

    assert response.status_code == 200
    assert response.json().get("access_token") is not None