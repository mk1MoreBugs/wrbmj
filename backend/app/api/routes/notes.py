from typing import Annotated

from fastapi import (
    APIRouter,
    Path,
    Query,
    WebSocketDisconnect,
)
from fastapi.websockets import WebSocket

from app.api.deps import TokenDep, SessionDep, RedisDep
from app.api.utils import note_utils
from app.api.utils.token_utils import check_token_data, get_token_data_or_raise_exception
from app.models.notes import NoteOutShort, NoteOutInDetailed
from app.crud import notes as notes_crud
from app.api.utils.connection_manager import ws_connection_manager as connection_manager

router = APIRouter(
    prefix="/notes",
    tags = ["notes"],
)


@router.get("/")
async def get_list_notes_for_user(
        token: TokenDep,
        session: SessionDep,
) -> list[NoteOutShort]:
    token_data = get_token_data_or_raise_exception(token=token)
    list_of_notes = notes_crud.get_notes_by_username(session=session, username=token_data.username)
    return list_of_notes


@router.post("/")
async def create_note(
        token: TokenDep,
        session: SessionDep,
) -> NoteOutInDetailed:
    token_data = get_token_data_or_raise_exception(token=token)
    note_in_db = note_utils.create_user_note(session=session, username=token_data.username)
    return NoteOutInDetailed.model_validate(note_in_db)


@router.websocket("/{note_id}/edit")
async def edit_note(
        note_id: Annotated[int, Path()],
        token: Annotated[str, Query()],
        websocket: WebSocket,
        session: SessionDep,
        redis: RedisDep,
):
    check_token_data(token=token)

    await connection_manager.connect(websocket)

    note = await note_utils.get_note(
        session=session,
        redis=redis,
        note_id=note_id,
    )
    if note is None:
        note_utils.raise_exception_note_dont_exist(note_id=note_id)

    note_in_detailed = NoteOutInDetailed.model_validate(note)

    await connection_manager.send_personal_message(note_in_detailed.model_dump_json(), websocket)

    old_note = note_in_detailed.model_copy()
    try:
        while True:
            await note_utils.update_note_from_ws(
                redis=redis,
                websocket=websocket,
                connection_manager=connection_manager,
                note_id=note_id,
            )

    except WebSocketDisconnect:
        await note_utils.save_note_from_redis_to_db(
            session=session,
            redis=redis,
            note_id=note_id,
            old_note=old_note,
        )
        connection_manager.disconnect(websocket)
