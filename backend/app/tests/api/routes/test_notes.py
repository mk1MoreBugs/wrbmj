from starlette.testclient import TestClient

from app.core.config import settings
from app.tests.utils.notes import create_test_note_from_api
from app.tests.utils.users import get_unique_username, create_test_user_and_get_auth_header


def test__edit_note__create_note_and_edit_note__get_updated_note(client: TestClient, unique_usernames: str):
    username = get_unique_username(unique_usernames=unique_usernames)
    password = "plain_password"
    auth_header = create_test_user_and_get_auth_header(
        client=client,
        username=username,
        plain_password=password,
    )
    test_note = create_test_note_from_api(client=client, auth_header=auth_header)

    websocket_connect = client.websocket_connect(
            url=f"{settings.API_V1_STR}/notes/{test_note.id}/edit",
            headers=auth_header,
    )
    with websocket_connect as websocket:
        new_note_content = "new note content"
        updated_note = test_note
        updated_note.note_content = new_note_content
        data = websocket.receive_json()
        websocket.close()
        assert data == test_note.model_dump()
