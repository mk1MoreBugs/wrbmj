from sqlmodel import Session

from app.core.security import get_password_hash
from app.crud import users
from app.models import UserInDb
from app.models.users import UserUpload


def create_test_user(db: Session, user: UserUpload):
    users_for_write_db = UserInDb(
        **dict(user),
        hashed_password=get_password_hash(password=user.plain_password),
        photo_file_name="path/to/file"
    )
    users.create_user(session=db, user=users_for_write_db)
