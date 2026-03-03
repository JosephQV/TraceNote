#
# Schemas (Pydantic models) for the API
#
import datetime

from pydantic import BaseModel, UUID4, EmailStr, Field, AwareDatetime
from typing import Annotated, Literal, List, Tuple


# TODO: where is uniqueness specified?

# notes for current implementation:
# Comments cannot be edited or have replies


# *** USER ENTITY TYPE ***
# The schema for a user object when it is inputted (received in a request)
class UserInput(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=30)]
    email: EmailStr
    account_visibility: Literal["default", "private", "public"] = "default"
    password: Annotated[str, Field(min_length=6, max_length=30)]

# The schema for a user object when it is outputted (sent in a response)
class UserOutput(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=30)]
    email: EmailStr
    account_visibility: Literal["default", "private", "public"] = "default"
    user_id: UUID4
    is_verified: bool = False
    account_status: Literal["enabled", "suspended"] = "enabled"
    created_datetime: AwareDatetime
    last_edited_datetime: AwareDatetime | None = None
    last_login_datetime: AwareDatetime = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
    friend_user_ids: Annotated[List[UUID4], Field(min_length=0, max_length=300)] = []
    liked_post_ids: Annotated[List[UUID4], Field(...)] = []
    bio_text: Annotated[str, Field(min_length=0, max_length=1000)] = ""
    media_object_key: str | None = None

class UserUpdate(BaseModel):
    bio_text: Annotated[str, Field(min_length=0, max_length=1000)] | None = None
    account_visibility: Literal["default", "private", "public"] | None = None

# The schema for a user object when it is in the database (all attributes)
class UserStored(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=30)]
    email: EmailStr
    account_visibility: Literal["default", "private", "public"] = "default"
    user_id: UUID4
    hashed_password: str
    is_verified: bool = False
    account_status: Literal["enabled", "suspended"] = "enabled"
    created_datetime: AwareDatetime
    last_edited_datetime: AwareDatetime | None = None
    last_login_datetime: AwareDatetime = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
    friend_user_ids: Annotated[List[UUID4], Field(min_length=0, max_length=300)] = []
    liked_post_ids: Annotated[List[UUID4], Field(...)] = []
    bio_text: Annotated[str, Field(min_length=0, max_length=1000)] = ""
    media_object_key: str | None = None


# *** POST ENTITY TYPE ***
class PostInput(BaseModel):
    text: Annotated[str, Field(min_length=0, max_length=1000)]
    created_location: Tuple[float, float]
    tags: Annotated[List[Literal['nature', 'art', 'event', 'music', 'travel', 'science', 'sports', 'cars', 'exercise', 'health']], Field(min_length=0, max_length=3)] = []
    availability_radius: int
    availability_timespan: Tuple[float, float]

class PostUpdate(BaseModel):
    post_id: UUID4
    text: Annotated[str, Field(min_length=0, max_length=1000)] | None = None
    tags: Annotated[List[Literal['nature', 'art', 'event', 'music', 'travel', 'science', 'sports', 'cars', 'exercise', 'health']], Field(min_length=0, max_length=3)] | None = None
    availability_radius: int | None = None
    availability_timespan: Tuple[float, float] | None = None

class PostStored(BaseModel):
    text: Annotated[str, Field(min_length=0, max_length=1000)]
    created_location: Tuple[float, float]
    tags: Annotated[List[Literal['nature', 'art', 'event', 'music', 'travel', 'science', 'sports', 'cars', 'exercise', 'health']], Field(min_length=0, max_length=3)] = []
    availability_radius: int
    availability_timespan: Tuple[float, float]
    post_id: UUID4
    author_id: UUID4
    media_object_key: str | None = None
    created_datetime: AwareDatetime
    last_edited_datetime: AwareDatetime | None = None
    expiration_datetime: AwareDatetime
    like_count: int = 0
    status: Literal["active", "archived"] = "active"
    post_visibility: Literal["default", "private", "public"]
    comment_ids: Annotated[List[UUID4], Field(...)] = []


# *** COMMENT ENTITY TYPE ***
class CommentStored(BaseModel):
    text: Annotated[str, Field(min_length=1, max_length=1000)]
    created_datetime: AwareDatetime
    comment_id: UUID4
    post_id: UUID4
    author_id: UUID4
    like_count: int = 0


# *** REPORT ENTITY TYPE ***
class ReportStored(BaseModel):
    report_id: UUID4
    author_type: Literal["user", "auto"]
    author_user_id: UUID4 | None = None
    subject: Literal["profile", "post", "comment"]
    subject_profile_id: UUID4 | None = None
    subject_post_id: UUID4 | None = None
    subject_comment_id: UUID4 | None = None
    created_datetime: AwareDatetime
    category: Literal["advertising-spam", "hate speech", "bullying", "inappropriate content"]
    reason: Annotated[str, Field(min_length=6, max_length=1000)]
    status: Literal["submitted", "action taken", "no action taken"]


# *** FRIEND_REQUEST ENTITY TYPE ***
class FriendRequestStored(BaseModel):
    sending_user_id: UUID4
    receiving_user_id: UUID4
    request_id: UUID4
    status: Literal["sent", "accepted", "rejected"] = "sent"
    created_date: AwareDatetime


# *** OTHER ***
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str