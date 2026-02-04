#
# Schemas (Pydantic models) for the API
#
from pydantic import BaseModel, UUID8, EmailStr


# The base schema for a user object
class UserBase(BaseModel):
    user_id: UUID8
    username: str
    email: EmailStr


# The schema for a user object when it is inputted (received in a request)
class UserInput(UserBase):
    password: str


# The schema for a user object when it is outputted (sent in a response)
class UserOutput(UserBase):
    pass


# The schema for a user object when it is in the database (all attributes)
class UserStored(UserBase):
    hashed_password: str



