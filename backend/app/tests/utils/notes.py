from datetime import datetime

from sqlmodel import Session

from app.crud.notes import create_note
from app.models.notes import NotesInDb


def create_test_note(
        db: Session,
        user_id: int,
        note_content: str,
        title_name: str | None = None,
) -> NotesInDb:
    test_note = NotesInDb(
        user_id=user_id,
        last_update=datetime.now(),
        note_content=note_content,
        title_name=title_name,
    )
    create_note(session=db, note=test_note)

    return test_note
