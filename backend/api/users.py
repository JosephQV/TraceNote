#
# API endpoints for users and profiles
#
from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
import jwt
from jwt.exceptions import InvalidTokenError

from api_schemas import UserUpdate, UserInput, UserOutput, UserStored, TokenData
from api.auth import oauth2_scheme
from config import JWT_ALGORITHM, JWT_SECRET_KEY
from services.users import get_user, add_user, update_user, add_media_object_key_to_user, delete_user
from database import upload_media_to_s3


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
    try:
        user = get_user(username=token_data.username)
    except:
        raise credentials_exception
    return user


@router_users.get("/self")
async def read_own_user(current_user: Annotated[UserStored, Depends(get_current_user)]) -> UserOutput:
    return UserOutput(**current_user.model_dump(exclude={"hashed_password"}))


@router_users.post("/signup")
async def create_user(new_user: UserInput) -> UserOutput:
    created_user = add_user(new_user)
    return created_user


@router_users.patch("/edit_user")
async def edit_own_user(
    current_user: Annotated[UserStored, Depends(get_current_user)],
    user_update: UserUpdate
) -> UserOutput:    
    try:
        updated_user = update_user(current_user.user_id, user_update)
    except:
        raise HTTPException(400, detail="Update operation failed")
    return UserOutput(**updated_user.model_dump(exclude={"hashed_password"}))


@router_users.post("/upload_media")
async def upload_media(
    current_user: Annotated[UserStored, Depends(get_current_user)],
    picture_file: UploadFile = File(...)
) -> dict:
    file_extension = picture_file.filename.split(".")[-1]
    object_key = f"users/{current_user.user_id}_{uuid.uuid4()}.{file_extension}"
    try:
        upload_media_to_s3(picture_file, object_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    add_media_object_key_to_user(current_user.user_id, object_key)

    return {"object_key": object_key}


@router_users.delete("/delete_user")
async def delete_own_user(
    current_user: Annotated[UserStored, Depends(get_current_user)]
) -> dict:
    delete_user(current_user.user_id)
    return {"Delete operation successful": current_user.user_id}