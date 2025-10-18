from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class BaseUser(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=42, unique=True)


class UserInDb(BaseUser, table=True):
    __tablename__ = "users"

    hashed_password: str
    photo_file_name: str


    notes: list["NoteInDb"] | None = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "primaryjoin": "UserInDb.id == NoteInDb.user_id",
            "foreign_keys": "[NoteInDb.user_id]"
        }
    )

class UserUpload(BaseUser):
    plain_password: str
    photo_file: bytes