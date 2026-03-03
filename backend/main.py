import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from api.auth import router_auth
from api.users import router_users
from api.posts import router_posts
from database import db_client, get_s3_media_url
from config import ENV_MODE


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


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/get_media_url/{object_key:path}")
async def get_media_url(object_key: str):
    try:
       result = get_s3_media_url(object_key)
    except:
        raise HTTPException(status_code=404, detail="Media file not found")
    return result


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0' if ENV_MODE == 'prod' else '127.0.0.1',
        port=8080,
        proxy_headers=True
    )