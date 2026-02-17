#
# API endpoints for posts and comments
#
from typing import Annotated

from fastapi import APIRouter, Depends

from .users import get_current_user
from ..services.posts import get_all_posts_for_user, add_post
from ..api_schemas import UserStored, PostStored, PostBase


router_posts = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router_posts.get("/my_posts")
async def read_own_posts(
    current_user: Annotated[UserStored, Depends(get_current_user)],
):
    return [PostStored(**post) for post in get_all_posts_for_user(current_user)]


@router_posts.post("/create_post")
async def create_post(
    current_user: Annotated[UserStored, Depends(get_current_user)],
    new_post: PostBase
) -> PostStored:
    return add_post(new_post, current_user)