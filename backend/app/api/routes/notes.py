from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    WebSocketDisconnect,
)
from fastapi.websockets import WebSocket

from app.api.deps import reusable_oauth2, TokenDep, WsConnectionManagerDep, SessionDep
from app.api.utils.note_utils import create_user_note, raise_exception_note_dont_exist, update_note_from_ws
from app.api.utils.token_utils import check_token_data, get_token_data_or_raise_exception
from app.models.notes import NotesOutShort, NotesOutInDetailed
from app.crud import notes as notes_crud


router = APIRouter(
    prefix="/notes",
    tags = ["notes"],
)


@router.get("/")
async def get_list_notes_for_user(token: Annotated[str, Depends(reusable_oauth2)]) -> list[NotesOutShort]:
    pass


@router.post("/")
async def create_note(
        token: TokenDep,
        session: SessionDep,
) -> NotesOutInDetailed:
    token_data = get_token_data_or_raise_exception(token=token)
    note_in_db = create_user_note(session=session, username=token_data.username)
    return NotesOutInDetailed.model_validate(note_in_db)


@router.websocket("/{note_id}/edit")
async def edit_note(
        note_id: Annotated[int, Path()],
        token: TokenDep,
        websocket: WebSocket,
        connection_manager: WsConnectionManagerDep,
        session: SessionDep,
):
    check_token_data(token=token)

    await connection_manager.connect(websocket)

    # TODO: get note in redis

    note_from_db = notes_crud.get_note_by_id(session=session, note_id=note_id)
    note_out_in_detailed = NotesOutInDetailed.model_validate(note_from_db)

    # TODO: save it in redis

    if note_from_db is None:
        raise_exception_note_dont_exist(note_id=note_id)

    await connection_manager.send_personal_message(note_out_in_detailed.model_dump_json(), websocket)

    try:
        old_note = note_out_in_detailed.model_copy()
        while True:
            old_note = await update_note_from_ws(
                session=session,
                websocket=websocket,
                connection_manager=connection_manager,
                note_id=note_id,
                old_note=old_note,
            )

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
