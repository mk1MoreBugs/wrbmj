from datetime import datetime, timedelta, timezone
from typing import Any
import jwt

from config import settings


ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# TODO implement with bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pass


def get_password_hash(password: str) -> str:
    pass
