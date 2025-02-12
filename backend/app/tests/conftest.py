from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from ..core.config import settings
from app.core.db import get_engine
from app.main import app
from app.models import UserInDb
from app.core.db import SQLModel

@pytest.fixture(scope="package")
def db() -> Generator[Session, None, None]:
    """
    before crud tests:
        docker exec -it wrbmj-db-1 \
        psql -U postgres \
        -c "CREATE DATABASE test_database;"

    after:
        docker exec -it wrbmj-db-1 \
        psql -U postgres \
        -c "DROP DATABASE test_database;"
    """

    old_path = settings.POSTGRES_DB
    test_db = "test_database"
    settings.set_db_path(path=test_db)
    engine = get_engine(echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    settings.set_db_path(path=old_path)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def user() -> UserInDb:
    return  UserInDb(
        username="user_name",
        hashed_password="hashed_password",
        photo_file_name="path/to/file"
    )