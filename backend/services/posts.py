from typing import List
import uuid
import datetime
import math

from pydantic import UUID4

from api_schemas import UserStored, PostBase, PostStored, PostUpdate
from db.session import users_collection, posts_collection


def add_post(new_post: PostBase, user: UserStored) -> PostStored:
    created_datetime_ = datetime.datetime.now(datetime.timezone.utc)
    new_stored_post = PostStored(
        **new_post.model_dump(), 
        post_id=uuid.uuid4(),
        author_id=user.user_id,
        created_datetime=created_datetime_,
        expiration_datetime=created_datetime_ + datetime.timedelta(hours=new_post.availability_timespan),
        post_visibility=user.account_visibility
    )
    posts_collection.insert_one(new_stored_post.model_dump())
    return new_stored_post


def update_post(post_update: PostUpdate) -> PostStored:
    posts_collection.update_one(
        filter={"post_id": post_update.post_id},
        update={"$set": post_update.model_dump()},
    )
    updated_post = get_post(post_update.post_id)
    return updated_post


def delete_post(post_id: UUID4):
    result = posts_collection.delete_one({"post_id": post_id})


def get_post(post_id: UUID4) -> PostStored:
    with posts_collection.find({"post_id": post_id}) as cursor:
        posts = [PostStored(**post) for post in cursor]
    assert len(posts) != 0, f"POST with post_id '{post_id}' not found."
    return posts[0]


def get_all_posts_for_user(user: UserStored) -> list[PostStored]:
    with posts_collection.find({"author_id": user.user_id}) as cursor:
        posts = [PostStored(**post) for post in cursor]
    return posts


def increment_post_likes(post_id: str, liking_user: UserStored) -> PostStored:
    assert post_id not in liking_user.liked_post_ids
    like_post_result = posts_collection.update_one(
        filter={"post_id": UUID4(post_id)},
        update={"$inc": {"like_count": 1}} # increment likes by 1
    )
    user_likes_result = users_collection.update_one(
        filter={"user_id": liking_user.user_id},
        update={"$push": {"liked_post_ids": post_id}}
    )
    # print(like_post_result)
    # print(user_likes_result)
    return get_post(UUID4(post_id))


def retrieve_posts_near_location(latitude: float, longitude: float) -> list[PostStored]:
    # retrieve all posts
    nearby_posts = []
    # sift through them to find the ones that are nearby, depending on each
    # post's created_location, the inputted location (latitude, longitude) args,
    # and the post's availability_radius.
    with posts_collection.find() as cursor:
        for post in cursor:
            post_lat, post_lon = post["created_location"]
            distance = math.sqrt((post_lat - latitude)**2 + (post_lon - longitude)**2)
            if distance < post["availability_radius"]:
                nearby_posts.append(PostStored(**post))
    return nearby_posts