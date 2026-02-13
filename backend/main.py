from fastapi import FastAPI

from .api.auth import router_auth
from .api.users import router_users
from .api.posts import router_posts
from .db.session import db_client
from .api_schemas import UserBase

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_posts)

db = db_client.Trace