from sqlmodel import create_engine
from app.models import User

from app.core.config import settings


def get_engine(echo=False):
    return create_engine(url=str(settings.SQLALCHEMY_DATABASE_URI), echo=echo)
