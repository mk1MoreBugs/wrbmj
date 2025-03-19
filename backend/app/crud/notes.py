from sqlalchemy import Select
from sqlmodel import Session, select

from app.models import UserInDb
from app.models.notes import NotesOutInDetailed, NotesInDb, NotesOutShort


def create_note(session: Session, note: NotesInDb) -> None:
    session.add(note)
    session.commit()
    session.refresh(note)


def get_note_by_id(session: Session, note_id: int) -> NotesOutInDetailed | None:
    statement: Select = select(NotesInDb).where(NotesInDb.id == note_id)
    note: NotesOutInDetailed | None = session.exec(statement).first()
    return note


def get_notes_by_username(session: Session, username: str) -> list[NotesOutShort | None]:
    statement: Select = select(NotesInDb).join(UserInDb, NotesInDb.user_id == UserInDb.id).where(UserInDb.username == username)
    notes: list[NotesOutInDetailed | None] = list(session.exec(statement).all())
    return notes
