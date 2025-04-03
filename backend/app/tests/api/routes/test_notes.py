import json

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from starlette.testclient import WebSocketDenialResponse

from app.core.config import settings
from app.models.notes import NoteOutInDetailed
from app.tests.utils.notes import create_test_note_from_api
from app.tests.utils.users import get_unique_username, create_test_user_and_get_auth_header


def test__get_list_notes_for_user__create_2_note_and_make_request_with_auth_token__return_200_status_code(client: TestClient, unique_usernames: str):
    username = get_unique_username(unique_usernames=unique_usernames)
    password = "plain_password"
    auth_header = create_test_user_and_get_auth_header(
        client=client,
        username=username,
        plain_password=password,
    )
    create_test_note_from_api(client=client, auth_header=auth_header)
    create_test_note_from_api(client=client, auth_header=auth_header)

    response = client.get(
        url=f"{settings.API_V1_STR}/notes",
        headers=auth_header,
    )
    response_body = response.json()

    assert response.status_code == 200
    assert len(response_body) == 2


def test__get_list_notes_for_user__make_request_without_auth_token__return_401_status_code(client: TestClient, unique_usernames: str):
    response = client.get(url=f"{settings.API_V1_STR}/notes")
    response_body = response.json()

    assert response.status_code == 401
    assert response_body["detail"] == "Not authenticated"


def test__edit_note__create_note_and_load_note__get_empty_note(client: TestClient, unique_usernames: str):
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
        data_websocket: str = websocket.receive_json()
        notes_out_in_detailed: NoteOutInDetailed = NoteOutInDetailed.model_validate_json(data_websocket)

        assert notes_out_in_detailed.last_update == test_note.last_update
        assert notes_out_in_detailed.id == test_note.id
        assert notes_out_in_detailed.title_name == test_note.title_name
        assert notes_out_in_detailed.note_content == test_note.note_content
        assert len(notes_out_in_detailed.model_dump()) == 4


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
        new_note_title = "new note title"
        updated_note = test_note.model_copy(
            update={
                "note_content": new_note_content,
                "title_name": new_note_title
            }
        ).model_dump_json()

        websocket.receive_json()
        websocket.send_json(updated_note)
        data_websocket: str = websocket.receive_json()
        notes_out_in_detailed: NoteOutInDetailed = NoteOutInDetailed.model_validate_json(data_websocket)

        assert notes_out_in_detailed.last_update != test_note.last_update
        assert notes_out_in_detailed.id == test_note.id
        assert notes_out_in_detailed.title_name == new_note_title
        assert notes_out_in_detailed.note_content == new_note_content
        assert len(notes_out_in_detailed.model_dump()) == 4


def test__edit_note__client_send_data_without_required_fields__get_validation_exception(client: TestClient, unique_usernames: str):
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
        updated_note = test_note.model_dump()
        updated_note["last_update"] = updated_note["last_update"].isoformat()
        del updated_note["title_name"]
        updated_note_json = json.dumps(updated_note)

        websocket.receive_json()
        with pytest.raises(ValidationError) as e:
            websocket.send_json(updated_note_json)
            websocket.receive_json()

        assert "Field required" in str(e.value)


def test__edit_note__attempt_to_create_note_without_user_auth__get_401_auth_exception(client: TestClient, unique_usernames: str):
    response = client.post(url=f"{settings.API_V1_STR}/notes")
    assert response.status_code == 401


def test__edit_note__attempt_to_edit_note_without_user_auth__get_websocket_denial_response_exception(client: TestClient, unique_usernames: str):
    username = get_unique_username(unique_usernames=unique_usernames)
    password = "plain_password"
    auth_header = create_test_user_and_get_auth_header(
        client=client,
        username=username,
        plain_password=password,
    )
    test_note = create_test_note_from_api(client=client, auth_header=auth_header)

    websocket_connect = client.websocket_connect(url=f"{settings.API_V1_STR}/notes/{test_note.id}/edit")
    with pytest.raises(WebSocketDenialResponse):
        with websocket_connect:
            pass
