from datetime import datetime
from typing import Optional, Annotated

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.types import Text


class BaseNote(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    last_update: datetime
    title_name: Optional[str] = Field(max_length=84)


class NoteInDb(BaseNote, table=True):
    __tablename__ = "notes"

    user_id: Annotated[int, Field(foreign_key="users.id")]
    note_content: Annotated[str, Field(sa_type=Text)]

    user: "UserInDb" = Relationship(
        back_populates="notes",
        sa_relationship_kwargs={
            "primaryjoin":"UserInDb.id == NoteInDb.user_id",
            "foreign_keys":"[NoteInDb.user_id]"
        }
    )


class NoteOutShort(BaseNote):
    short_description: str


class NoteOutInDetailed(BaseNote):
    note_content: str
