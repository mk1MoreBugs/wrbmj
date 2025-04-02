import datetime

from sqlalchemy import Select
from sqlmodel import Session, select, update

from app.models import UserInDb
from app.models.notes import NotesOutInDetailed, NotesInDb, NotesOutShort


def create_note(session: Session, note: NotesInDb) -> None:
    session.add(note)
    session.commit()
    session.refresh(note)


def get_note_by_id(session: Session, note_id: int) -> NotesOutInDetailed | None:
    statement: Select = select(NotesInDb).where(NotesInDb.id == note_id)
    note_in_db: NotesInDb | None = session.exec(statement).first()
    return __get_note_out_or_none(note_in_db)

def __get_note_out_or_none(note_in_db: NotesInDb) -> NotesOutInDetailed | None:
    if note_in_db is None:
        return None
    else:
        return NotesOutInDetailed.model_validate(note_in_db)


def get_notes_by_username(session: Session, username: str) -> list[NotesOutShort | None]:
    statement: Select = (
        select(NotesInDb).join(UserInDb, NotesInDb.user_id == UserInDb.id)
                         .where(UserInDb.username == username)
    )
    notes: list[NotesOutInDetailed | None] = list(session.exec(statement).all())
    return notes


def update_content_note_by_id(session: Session, note_id: int, note_text: str, timestamp: datetime):
    statement = update(NotesInDb).where(NotesInDb.id == note_id).values(
        {
            "note_content": note_text,
            "last_update": timestamp,
        }
    )
    session.exec(statement)
    session.commit()


def update_title_note_by_id(session: Session, note_id: int, title_note: str, timestamp: datetime):
    statement = update(NotesInDb).where(NotesInDb.id == note_id).values(
        {
            "title_name": title_note,
            "last_update": timestamp,
        }
    )
    session.exec(statement)
    session.commit()
