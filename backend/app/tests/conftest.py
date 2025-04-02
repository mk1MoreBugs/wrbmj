from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from ..core.config import settings
from app.core.db import get_engine
from app.main import app
from app.core.db import SQLModel
from ..models.users import UserUpload


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

    settings.set_db_host(host="localhost")
    old_path = settings.POSTGRES_DB
    test_db = "test_database"
    settings.set_db_path(path=test_db)
    engine = get_engine(echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    settings.set_db_host(host="db")
    settings.set_db_path(path=old_path)


@pytest.fixture(scope="package")
def client() -> Generator[TestClient, None, None]:
    settings.set_db_host(host="localhost")
    test_db = "test_database"
    settings.set_db_path(path=test_db)
    engine = get_engine(echo=True)
    SQLModel.metadata.create_all(engine)

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def user() -> UserUpload:
    return  UserUpload(
        username="user_name",
        plain_password="hashed_password",
        photo_file= b"photo_file"
    )


@pytest.fixture(scope="session")
def unique_usernames() -> set[str]:
    return set()
