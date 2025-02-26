from typing import Annotated
from fastapi import APIRouter, Depends, Path

from app.api.deps import reusable_oauth2
from app.models.notes import NotesOutShort, NotesOutInDetailed


router = APIRouter(
    prefix="/notes",
    tags = ["notes"],
)


@router.get("/")
async def get_list_notes_for_user(token: Annotated[str, Depends(reusable_oauth2)]) -> list[NotesOutShort]:
    pass


@router.websocket("/{note_id}")
async def get_note_by_id(
        note_id: Annotated[str, Path()],
        token: Annotated[str, Depends(reusable_oauth2)]
) -> NotesOutInDetailed:
    # check user token

    # get note in redis

        # if note exist in redis then get note from db
            # and save in redis

        # if note don't exist in db then send error

    # if Ok then send note
    pass


@router.put("/")
async def update_note(
        data: NotesOutInDetailed,
        token: Annotated[str, Depends(reusable_oauth2)]
) -> dict[str, str]:
    # check user token

    # save note in redis, ex=None

    # save note in db

    pass
