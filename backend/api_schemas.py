#
# Schemas (Pydantic models) for the API
#
from pydantic import BaseModel, UUID8, EmailStr
from typing import Annotated, Literal


# *** USER ENTITY TYPE ***

# The base schema for a user object
class UserBase(BaseModel):
    user_id: UUID8
    username: str # need to annotate with length and uniqueness constraints
    email: EmailStr
    account_visibility: Literal["default", "private", "public"]
    is_admin: bool
    account_status: Literal["active", "suspended"]

# The schema for a user object when it is inputted (received in a request)
class UserInput(UserBase):
    password: str

# The schema for a user object when it is outputted (sent in a response)
class UserOutput(UserBase):
    pass

# The schema for a user object when it is in the database (all attributes)
class UserStored(UserBase):
    hashed_password: str


# *** POST ENTITY TYPE ***

class PostBase(BaseModel):
    pass

class PostInput(PostBase):
    pass

class PostOutput(PostBase):
    pass

class PostStored(PostBase):
    pass


# *** COMMENT ENTITY TYPE ***

class CommentBase(BaseModel):
    pass

class CommentInput(CommentBase):
    pass

class CommentOutput(CommentBase):
    pass

class CommentStored(CommentBase):
    pass


# *** PROFILE ENTITY TYPE ***

class ProfileBase(BaseModel):
    pass

class ProfileInput(ProfileBase):
    pass

class ProfileOutput(ProfileBase):
    pass

class ProfileStored(ProfileBase):
    pass


# *** REPORT ENTITY TYPE ***

class ReportBase(BaseModel):
    pass

class ReportInput(ReportBase):
    pass

class ReportOutput(ReportBase):
    pass

class ReportStored(ReportBase):
    pass


# Other

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None