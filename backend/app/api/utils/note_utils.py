import datetime
import logging

from fastapi import (
    HTTPException,
    status,
    WebSocket
)
from redis.asyncio import Redis
from sqlmodel import Session

from app.api.utils import redis_utils
from app.api.utils.connection_manager import WsConnectionManager
from app.crud.users import get_user_by_username
from app.crud import notes as notes_crud
from app.models.notes import NoteInDb, NoteOutInDetailed


async def get_note(
        session: Session,
        redis: Redis,
        note_id: int,
) -> NoteOutInDetailed | None:
    note_from_redis: NoteOutInDetailed | None = await redis_utils.get_note_in_redis(redis=redis, note_id=note_id)

    if note_from_redis is None:
        note_from_db = await get_note_from_db_and_set_in_redis(session=session, redis=redis, note_id=note_id)
        return note_from_db
    return note_from_redis


async def get_note_from_db_and_set_in_redis(
        session: Session,
        redis: Redis,
        note_id: int,
) -> NoteOutInDetailed | None:
    note: NoteOutInDetailed | None = notes_crud.get_note_by_id(session=session, note_id=note_id)
    if note is not None:
        await redis_utils.set_note_in_redis(redis=redis, note_id=note_id, note_in_detailed=note)
    return note


def create_user_note(
        session: Session,
        username: str,
        note_content: str = "",
) -> NoteInDb:
    user = get_user_by_username(session=session, username=username)
    new_note = NoteInDb(
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
        redis: Redis,
        websocket: WebSocket,
        connection_manager: WsConnectionManager,
        note_id: int,
) -> NoteOutInDetailed:
    note_from_websocket = await websocket.receive_text()
    note_model = NoteOutInDetailed.model_validate_json(note_from_websocket, strict=True)
    current_timestamp = get_current_timestamp()
    note_model.last_update = current_timestamp

    await redis_utils.set_note_in_redis(redis=redis, note_id=note_id, note_in_detailed=note_model)

    await connection_manager.broadcast(message=note_model.model_dump_json())

    logger = logging.getLogger(__name__)
    logger.info("Note saved")

    return note_model


def get_current_timestamp():
    return datetime.datetime.now()


async def save_note_from_redis_to_db(
        session: Session,
        redis: Redis,
        note_id: int,
        old_note: NoteOutInDetailed
) -> None:
    note_in_redis: NoteOutInDetailed = await redis_utils.get_and_delete_note_in_redis(redis=redis, note_id=note_id)
    update_note_fields_in_db(session=session, note_id=note_id, old_note=old_note, new_note=note_in_redis)


def update_note_fields_in_db(
        session: Session,
        note_id: int,
        old_note: NoteOutInDetailed,
        new_note: NoteOutInDetailed,
) -> None:
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
