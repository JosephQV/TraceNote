import pathlib

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from ..creds import MONGO_USER, MONGO_PASSWORD
    

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@trace.rdifolj.mongodb.net/?appName=Trace"

# Create a new client and connect to the server
db_client = MongoClient(uri, server_api=ServerApi('1'), uuidRepresentation='standard', tz_aware=True)

db = db_client.test
users_collection = db.get_collection('users')
posts_collection = db.get_collection('posts')