from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import reusable_oauth2
from app.core.security import decode_jwt_token


router = APIRouter(
    prefix="/users",
    tags = ["users"],
)

@router.get("/")
async def get_user_info(token: Annotated[str, Depends(reusable_oauth2)]):
    token_data = decode_jwt_token(token=token)
    if token_data is not None:
        return token_data
    else:
        return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
