from sqlmodel import create_engine
from app.models import User

from app.core.config import settings


def get_engine():
    return create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
