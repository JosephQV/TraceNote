import pathlib

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from ..creds import MONGO_USER, MONGO_PASSWORD
    

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@trace.rdifolj.mongodb.net/?appName=Trace"

# Create a new client and connect to the server
db_client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    db_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = db_client.test
    print(db)
    col = db.get_collection('users')
    print(col)
    col.insert_one({'x': 1})
except Exception as e:
    print(e)