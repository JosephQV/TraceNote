#
# API endpoints for posts and comments
#
from typing import Annotated

from fastapi import APIRouter, Depends

from .users import get_current_user
from services.posts import get_all_posts_for_user
from api_schemas import UserBase


router_posts = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router_posts.get("/my_posts")
async def read_own_items(
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    return get_all_posts_for_user(current_user.username)