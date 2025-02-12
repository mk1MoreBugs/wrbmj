from sqlalchemy import Select
from sqlmodel import Session, select

from app.models.users import User


def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(session: Session, user_id: int) -> User | None:
    statement: Select = select(User).where(User.id == user_id)
    session_user = session.exec(statement).first()
    return session_user