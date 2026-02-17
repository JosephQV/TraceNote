#
# API endpoints for users and profiles
#
from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError

from ..api_schemas import UserBase, UserInput, UserOutput, UserStored, TokenData
from ..api.auth import oauth2_scheme
from ..creds import JWT_ALGORITHM, JWT_SECRET_KEY
from ..services.users import get_user, add_user


router_users = APIRouter(
    prefix="/users",
    tags=["users"]
)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserStored:
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
    return UserStored(**user)


@router_users.get("/self")
async def read_own_user(current_user: Annotated[UserStored, Depends(get_current_user)]) -> UserOutput:
    return UserOutput(**current_user.model_dump(exclude={"hashed_password"}))


@router_users.post("/signup")
async def create_user(new_user: UserInput) -> UserOutput:
    created_user = add_user(new_user)
    return created_user