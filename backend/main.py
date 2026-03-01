import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import creds
from api.auth import router_auth
from api.users import router_users
from api.posts import router_posts
from db.session import db_client
from api_schemas import UserBase


db = db_client.Trace

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_posts)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("JWT_SECRET_KEY", "default"))


@app.get("/health")
async def health_check():
    return {"status": "ok"}