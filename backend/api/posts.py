#
# API endpoints for posts and comments
#
from typing import Annotated

from pydantic import UUID4
from fastapi import APIRouter, Depends, HTTPException

from .users import get_current_user
from ..services.posts import (
    get_post,
    get_all_posts_for_user, 
    add_post, 
    update_post,
    delete_post,
    increment_post_likes, 
    retrieve_posts_near_location
)
from ..api_schemas import UserStored, PostStored, PostBase, PostUpdate


router_posts = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router_posts.get("/my_posts")
async def read_own_posts(
    current_user: Annotated[UserStored, Depends(get_current_user)],
) -> list[PostStored]:
    return get_all_posts_for_user(current_user)


@router_posts.post("/create_post")
async def create_post(
    current_user: Annotated[UserStored, Depends(get_current_user)],
    new_post: PostBase
) -> PostStored:
    return add_post(new_post, current_user)


@router_posts.patch("/edit_post")
async def edit_own_post(
    current_user: Annotated[UserStored, Depends(get_current_user)],
    updated_post: PostUpdate
) -> PostStored:
    post = get_post(updated_post.post_id)
    if post.author_id != current_user.user_id:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized - Cannot edit non-authored post."
        )
    return update_post(updated_post)


@router_posts.delete("/delete_post/{post_id}")
async def delete_own_post(
    current_user: Annotated[UserStored, Depends(get_current_user)],
    post_id: str
) -> dict:
    post = get_post(UUID4(post_id))
    if post.author_id != current_user.user_id:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized - Cannot delete non-authored post."
        )
    delete_post(UUID4(post_id))
    return {"Delete operation successful": post_id}


@router_posts.patch("/like_post/{post_id}")
async def like_post(
    current_user: Annotated[UserStored, Depends(get_current_user)],
    post_id: str
) -> PostStored:
    return increment_post_likes(post_id, current_user)


@router_posts.get("/accessible_posts")
async def get_accessible_posts(
    current_user: Annotated[UserStored, Depends(get_current_user)],
    user_latitude: float,
    user_longitude: float
) -> list[PostStored]:
    # retrieve posts that are close enough to the user
    nearby_posts = retrieve_posts_near_location(user_latitude, user_longitude)
    # ensure each nearby post is active (not archived)
    active = [post for post in nearby_posts if post.status == "active"]
    # ensure each nearby active post is also visible to the current user 
    # based on the post_visibility setting (public, private, or default)
    visible = []
    for post in active:
        # the post_visibility is "public" or "default", so it is visible
        if post.post_visibility != "private":
            visible.append(post)
        # the post is "private" but was created by a friend, so it is visible
        elif post.author_id in current_user.friend_user_ids:
            visible.append(post)
    return visible