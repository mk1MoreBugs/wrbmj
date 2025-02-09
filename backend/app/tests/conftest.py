from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from ..core.config import settings
from app.core.db import get_engine
from app.main import app
from app.models import SQLModel
from sqlalchemy import text

@pytest.fixture()
def db() -> Generator[Session, None, None]:
    old_path = settings.POSTGRES_DB
    test_db = "test_database"
    # in psql: CREATE DATABASE test_database;
    settings.set_db_path(path=test_db)
    engine = get_engine()
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # DROP DATABASE test_database;
    settings.set_db_path(path=old_path)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
