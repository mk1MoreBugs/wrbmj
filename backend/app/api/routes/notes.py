from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    Path,
    WebSocket,
)
from starlette.websockets import WebSocketDisconnect

from app.api.deps import reusable_oauth2, TokenDep, WsConnectionManagerDep
from app.api.utils.token_utils import get_token_data_or_raise_exception
from app.models.notes import NotesOutShort, NotesOutInDetailed

router = APIRouter(
    prefix="/notes",
    tags = ["notes"],
)


@router.get("/")
async def get_list_notes_for_user(token: Annotated[str, Depends(reusable_oauth2)]) -> list[NotesOutShort]:
    pass


@router.websocket("/edit")
async def get_note_by_id(
        note_id: Annotated[str, Path()],
        token: TokenDep,
        websocket: WebSocket,
        connection_manager: WsConnectionManagerDep,
):
    # check user token
    get_token_data_or_raise_exception(token=token)

    await connection_manager.connect(websocket)

    # TODO: get note in redis

    # TODO: if  note don't exist in redis then get note from db

        # TODO: and save in redis

    # TODO: if note don't exist in db save in redis response body

    # TODO: send note
    note = ""
    connection_manager.send_personal_message(note, websocket)

    try:
        while True:
            data = await websocket.receive_text()


            await connection_manager.broadcast(message=data)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
