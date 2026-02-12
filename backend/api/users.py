#
# API endpoints for users and profiles
#
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError

from api_schemas import UserBase
from api.auth import oauth2_scheme
from config import JWT_ALGORITHM, JWT_SECRET_KEY
from api_schemas import TokenData
from services.users import get_user


router_users = APIRouter(
    prefix="/users",
    tags=["users"]
)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router_users.get("/me")
async def read_users_me(current_user: Annotated[UserBase, Depends(get_current_user)]):
    return current_user


