from typing import List
import uuid
import datetime

from ..api_schemas import UserStored, PostBase, PostStored
from ..db.session import users_collection
from ..db.session import posts_collection


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


def get_all_posts_for_user(user: UserStored):
    return posts_collection.find({"author_id": user.user_id})