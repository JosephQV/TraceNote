#
# API endpoints for posts and comments
#
from typing import Annotated
import uuid

from pydantic import UUID4
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from .users import get_current_user
from services.posts import (
    get_post,
    get_all_posts_for_user, 
    add_post, 
    update_post,
    delete_post,
    increment_post_likes, 
    retrieve_posts_near_location,
    add_media_object_key_to_post
)
from api_schemas import UserStored, PostStored, PostInput, PostUpdate
from database import upload_media_to_s3


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
    new_post: PostInput
) -> PostStored:
    return add_post(new_post, current_user)


@router_posts.post("/upload_media")
async def upload_media(
    current_user: Annotated[UserStored, Depends(get_current_user)],
    parent_post_id: UUID4,
    file: UploadFile = File(...)
) -> dict:
    if get_post(parent_post_id).author_id != current_user.user_id:
        raise HTTPException(status_code=401, detail=f"Unauthorized - cannot upload media to non-authored post")
    
    file_extension = file.filename.split(".")[-1]
    object_key = f"posts/{current_user.user_id}_{parent_post_id}_{uuid.uuid4()}.{file_extension}"
    try:
        upload_media_to_s3(file, object_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    add_media_object_key_to_post(parent_post_id, object_key)

    return {"object_key": object_key}


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
    post = get_post(uuid.UUID(post_id))
    if post.author_id != current_user.user_id:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized - Cannot delete non-authored post."
        )
    try:
        delete_post(uuid.UUID(post_id))
    except:
        raise HTTPException(404, f"POST with post_id '{post_id}' not found")
    return {"Delete operation successful": post_id}


@router_posts.patch("/like_post/{post_id}")
async def like_post(
    current_user: Annotated[UserStored, Depends(get_current_user)],
    post_id: str
) -> PostStored:
    try:
        post = increment_post_likes(uuid.UUID(post_id), current_user)
    except:
        raise HTTPException(400, "Not allowed - cannot like an already liked post")
    return post


@router_posts.patch("/unlike_post/{post_id}")
async def unlike_post(
    current_user: Annotated[UserStored, Depends(get_current_user)],
    post_id: str
) -> PostStored:
    try:
        post = increment_post_likes(uuid.UUID(post_id), current_user, decrement=True)
    except:
        raise HTTPException(400, "Not allowed - cannot unlike an already unliked post")
    return post


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


# @router_posts.get("/accessible_posts_from_user")
# async def get_accessible_posts_from_user(
#         current_user: Annotated[UserStored, Depends(get_current_user)],
#         user_id: UUID4,
# ):
#     pass