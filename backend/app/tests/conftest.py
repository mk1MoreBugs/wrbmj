from collections.abc import Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlmodel import Session
from redis.asyncio.client import Redis

from ..core.config import settings
from app.core.db import get_engine
from app.main import app
from app.core.db import SQLModel
from ..models.users import UserUpload
from app.api.deps import get_redis

@pytest.fixture(scope="session")
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

    engine = get_engine(echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(scope="package")
def client() -> Generator[TestClient, None, None]:
    engine = get_engine(echo=True)
    SQLModel.metadata.create_all(engine)

    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture(loop_scope="session")
async def redis() -> Redis:
    return get_redis()


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
