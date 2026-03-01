import uuid
import datetime

import jwt
from pwdlib import PasswordHash
from pydantic import UUID4

from database import users_collection
from api_schemas import UserInput, UserOutput, UserStored, UserUpdate
from config import JWT_ALGORITHM, JWT_SECRET_KEY


password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return password_hash.hash(password)


def authenticate_user(username: str, password: str) -> UserStored:
    user = get_user(username)
    assert verify_password(password, user.hashed_password), "Authentication failed - incorrect password"
    return user


def create_access_token(data: dict, expires_delta: datetime.timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def add_user(new_user: UserInput) -> UserOutput:
    new_stored_user = UserStored(
        **new_user.model_dump(exclude={"password"}), 
        user_id=uuid.uuid4(),
        hashed_password=get_password_hash(new_user.password),
        created_datetime=datetime.datetime.now(datetime.timezone.utc)
    )
    users_collection.insert_one(new_stored_user.model_dump())
    return UserOutput(**new_stored_user.model_dump(exclude={"hashed_password"}))
    

def get_user(username: str) -> UserStored:
    record = users_collection.find_one({"username": username})
    assert record is not None, f"USER with username '{username}' not found"
    return UserStored(**record)


def update_user(user_id: UUID4, user_update: UserUpdate) -> UserStored:
    updated_user = users_collection.find_one_and_update(
        filter={"user_id": user_id},
        update={"$set": user_update.model_dump(exclude_none=True, exclude_unset=True)}
    )
    assert updated_user is not None
    return updated_user


def add_media_object_key_to_user(user_id: UUID4, media_object_key: str) -> UserStored:
    updated_user = users_collection.find_one_and_update(
        filter={"user_id": user_id},
        update={"$set": {"media_object_key": media_object_key}},
        return_document=True
    )
    assert updated_user is not None
    return UserStored(**updated_user)


def update_last_login(username: str):
    users_collection.update_one({"username": username}, update={"$set": {"last_login_datetime": datetime.datetime.now(datetime.timezone.utc)}})


def delete_user(user_id: UUID4):
    users_collection.delete_one(filter={"user_id": user_id})