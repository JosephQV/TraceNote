#
# Schemas (Pydantic models) for the API
#
from pydantic import BaseModel, UUID8, EmailStr, Field, PastDatetime
from typing import Annotated, Literal, List, Tuple


# TODO: where is uniqueness specified?
# TODO: how to organize input/output/stored model attributes?
# TODO: how to link media to post and profile attributes?

# notes for current implementation:
# comments cannot be edited or have replies


# *** USER ENTITY TYPE ***

# The base schema for a user object
class UserBase(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=30)]
    email: EmailStr
    account_visibility: Literal["default", "private", "public"] = "default"

# The schema for a user object when it is inputted (received in a request)
class UserInput(UserBase):
    password: Annotated[str, Field(min_length=6, max_length=30)]

# The schema for a user object when it is outputted (sent in a response)
class UserOutput(UserBase):
    pass

# The schema for a user object when it is in the database (all attributes)
class UserStored(UserBase):
    user_id: UUID8
    profile_id: UUID8 | None = None
    hashed_password: str
    is_admin: bool = False
    is_verified: bool = False
    account_status: Literal["enabled", "suspended"]
    created_datetime: PastDatetime
    last_login_datetime: PastDatetime
    friend_user_ids: Annotated[List[UUID8], Field(min_length=0, max_length=300)] = []


# *** POST ENTITY TYPE ***

class PostBase(BaseModel):
    text: Annotated[str, Field(min_length=0, max_length=1000)]
    created_location: Tuple[float, float]
    created_datetime: PastDatetime
    expiration_datetime: PastDatetime
    last_edited_datetime: PastDatetime
    tags: Annotated[List[Literal['nature', 'art', 'event', 'music', 'travel', 'science', 'sports', 'cars', 'exercise', 'health']], Field(min_length=0, max_length=3)] = []

class PostInput(PostBase):
    pass

class PostOutput(PostBase):
    pass

class PostStored(PostBase):
    post_id: UUID8
    author_id: UUID8
    like_count: int = 0
    status: Literal["active", "archived", "deleted"] = "active"
    post_visibility: Literal["default", "private", "public"] = "default"
    comment_ids: Annotated[List[UUID8], Field(...)] = []


# *** COMMENT ENTITY TYPE ***

class CommentBase(BaseModel):
    text: Annotated[str, Field(min_length=1, max_length=1000)]
    created_datetime: PastDatetime

class CommentInput(CommentBase):
    pass

class CommentOutput(CommentBase):
    pass

class CommentStored(CommentBase):
    comment_id: UUID8
    post_id: UUID8
    author_id: UUID8
    like_count: int = 0


# *** PROFILE ENTITY TYPE ***

class ProfileBase(BaseModel):
    bio: Annotated[str, Field(min_length=0, max_length=1000)]

class ProfileInput(ProfileBase):
    pass

class ProfileOutput(ProfileBase):
    pass

class ProfileStored(ProfileBase):
    profile_id: UUID8
    user_id: UUID8
    created_datetime: PastDatetime
    last_updated_datetime: PastDatetime


# *** REPORT ENTITY TYPE ***

class ReportBase(BaseModel):
    pass

class ReportInput(ReportBase):
    pass

class ReportOutput(ReportBase):
    pass

class ReportStored(ReportBase):
    report_id: UUID8
    author_type: Literal["user", "auto"]
    author_user_id: UUID8 | None = None
    subject: Literal["profile", "post", "comment"]
    subject_profile_id: UUID8 | None = None
    subject_post_id: UUID8 | None = None
    subject_comment_id: UUID8 | None = None
    created_datetime: PastDatetime
    category: Literal["advertising-spam", "hate speech", "bullying", "inappropriate content"]
    reason: Annotated[str, Field(min_length=6, max_length=1000)]
    status: Literal["submitted", "action taken", "no action taken"]


# *** FRIEND_REQUEST ENTITY TYPE ***

class FriendRequestBase(BaseModel):
    pass

class FriendRequestInput(FriendRequestBase):
    pass

class FriendRequestOutput(FriendRequestBase):
    pass

class FriendRequestStored(FriendRequestBase):
    sending_user_id: UUID8
    receiving_user_id: UUID8
    request_id: UUID8
    status: Literal["sent", "accepted", "rejected"] = "sent"
    created_date: PastDatetime


# Other

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None