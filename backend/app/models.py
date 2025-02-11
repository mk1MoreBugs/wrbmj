from sqlmodel import Field, SQLModel
from pydantic import BaseModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=42)
    hashed_password: str
    photo_file: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None