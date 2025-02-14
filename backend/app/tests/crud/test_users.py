from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
import pytest

from app.crud import users
from app.models.users import UserUpload
from app.tests.utils.users import create_test_user, get_unique_username


def test_create_user_and_get_user_from_db_return_user(db: Session, unique_usernames: str) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    create_test_user(db=db, username=username, plain_password="plain_password")
    user_in_db = users.get_user_by_username(session=db, username=username)
    assert user_in_db.username == username


def test_create_non_unique_user_return_error(db: Session, unique_usernames: str) -> None:
    username = get_unique_username(unique_usernames=unique_usernames)
    with pytest.raises(IntegrityError):
        create_test_user(db=db, username=username, plain_password="plain_password")
        create_test_user(db=db, username=username, plain_password="plain_password")
