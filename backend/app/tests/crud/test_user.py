from sqlmodel import Session

from app import crud
from app.crud import get_user_by_id
from app.models import User


def test_create_user(db: Session, user: User) -> None:
    crud.create_user(session=db, user=user)
    user_in_db = get_user_by_id(session=db,user_id=user.id)
    assert user_in_db.id == user.id
