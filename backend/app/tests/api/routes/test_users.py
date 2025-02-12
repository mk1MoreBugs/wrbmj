from starlette.testclient import TestClient

from app.core.config import settings
from app.models import UserInDb


def test_user_info(client: TestClient, user: UserInDb) -> None:
    response = client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == 200