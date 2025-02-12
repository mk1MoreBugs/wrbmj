from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
import pytest

from app.crud import users
from app.models.users import UserUpload
from app.tests.utils.users import create_test_user


def test_create_user_and_get_user_from_db_return_user(db: Session, user: UserUpload) -> None:
    create_test_user(db=db, user=user)
    user_in_db = users.get_user_by_username(session=db, username=user.username)
    assert user_in_db.username == user.username


def test_create_non_unique_user_return_error(db: Session, user: UserUpload) -> None:
    with pytest.raises(IntegrityError):
        create_test_user(db=db, user=user)
        create_test_user(db=db, user=user)
