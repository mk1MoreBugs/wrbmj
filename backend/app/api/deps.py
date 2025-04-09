from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from redis.asyncio.client import Redis

from app.api.utils.CustomOAuth2PasswordBearer import CustomOAuth2PasswordBearer
from app.core.config import settings
from app.core.db import get_engine
from app.api.utils.connection_manager import WsConnectionManager

reusable_oauth2 = CustomOAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


def get_db() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session

def get_redis() -> Redis:
    return Redis(
        host=settings.REDIS_DB,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        username=settings.REDIS_USER,
        password=settings.REDIS_PASSWORD,
    )


SessionDep = Annotated[Session, Depends(get_db)]
RedisDep = Annotated[Redis, Depends(get_redis)]

TokenDep = Annotated[str, Depends(reusable_oauth2)]
WsConnectionManagerDep = Annotated[WsConnectionManager, Depends(WsConnectionManager)]
