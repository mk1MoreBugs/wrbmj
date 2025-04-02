import datetime

from fastapi import (
    HTTPException,
    status,
    WebSocket
)
from sqlmodel import Session

from app.api.deps import WsConnectionManagerDep
from app.crud.users import get_user_by_username
from app.crud import notes as notes_crud
from app.models.notes import NotesInDb, NotesOutInDetailed


def create_user_note(
        session: Session,
        username: str,
        note_content: str = "",
) -> NotesInDb:
    user = get_user_by_username(session=session, username=username)
    new_note = NotesInDb(
        last_update=datetime.datetime.now(),
        user_id=user.id,
        note_content=note_content,
    )
    notes_crud.create_note(session=session, note=new_note)
    return new_note


def raise_exception_note_dont_exist(note_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Note with id {note_id} don't exist",
    )


async def update_note_from_ws(
        session: Session,
        websocket: WebSocket,
        connection_manager: WsConnectionManagerDep,
        note_id: int,
        old_note: NotesOutInDetailed,
) -> NotesOutInDetailed:
    note_from_websocket = await websocket.receive_json()
    new_note = NotesOutInDetailed.model_validate_json(note_from_websocket, strict=True)
    current_timestamp = get_current_timestamp()
    new_note.last_update = current_timestamp

    update_db_fields(
        session=session,
        note_id=note_id,
        old_note=old_note,
        new_note=new_note,
    )

    await connection_manager.broadcast(message=new_note.model_dump_json())
    return new_note


def get_current_timestamp():
    return datetime.datetime.now()


def update_db_fields(
        session: Session,
        note_id: int,
        old_note: NotesOutInDetailed,
        new_note: NotesOutInDetailed,
):
    if old_note.note_content != new_note.note_content:
        notes_crud.update_content_note_by_id(
            session=session,
            note_id=note_id,
            note_text=new_note.note_content,
            timestamp=new_note.last_update,
        )

    if old_note.title_name != new_note.title_name:
        notes_crud.update_title_note_by_id(
            session=session,
            note_id=note_id,
            title_note=new_note.title_name,
            timestamp=new_note.last_update,
        )
