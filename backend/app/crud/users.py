from sqlalchemy import Select
from sqlmodel import Session, select

from app.models.users import UserInDb


def create_user(session: Session, user: UserInDb) -> UserInDb:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(session: Session, user_id: int) -> UserInDb | None:
    statement: Select = select(UserInDb).where(UserInDb.id == user_id)
    session_user = session.exec(statement).first()
    return session_user