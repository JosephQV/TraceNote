import uuid
import datetime
import jwt
from pwdlib import PasswordHash

from ..db.session import users_collection
from ..api_schemas import UserBase, UserInput, UserOutput, UserStored
from ..creds import JWT_ALGORITHM, JWT_SECRET_KEY


password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def authenticate_user(username: str, password: str) -> dict | None:
    user = get_user(username)
    if user is None:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(data: dict, expires_delta: datetime.timedelta):
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
    

def get_user(username: str):
    return users_collection.find_one({"username": username})


def update_last_login(username: str):
    users_collection.update_one({"username": username}, update={"$set": {"last_login_datetime": datetime.datetime.now(datetime.timezone.utc)}})