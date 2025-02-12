from sqlmodel import Session

from app.crud import users
from app.models import UserInDb


def test_create_user(db: Session, user: UserInDb) -> None:
    users.create_user(session=db, user=user)
    user_in_db = users.get_user_by_id(session=db,user_id=user.id)
    assert user_in_db.id == user.id
