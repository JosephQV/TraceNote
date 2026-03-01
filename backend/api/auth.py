#
# API endpoints for authentication and security
#
from typing import Annotated
from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from services.users import authenticate_user, create_access_token, update_last_login
from api_schemas import Token
from config import ACCESS_TOKEN_EXPIRE_MINUTES


router_auth = APIRouter(
    tags=["auth"]
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router_auth.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    try:
        user = authenticate_user(form_data.username, form_data.password)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    update_last_login(form_data.username)
    return Token(access_token=access_token, token_type="bearer")
