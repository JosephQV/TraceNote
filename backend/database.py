import pathlib

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import boto3

from config import MONGO_USER, MONGO_PASSWORD, AWS_BUCKET_NAME
    

mongodb_uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@trace.rdifolj.mongodb.net/?appName=Trace"

s3_client = boto3.client('s3')


# Create a new client and connect to the server
db_client = MongoClient(mongodb_uri, server_api=ServerApi('1'), uuidRepresentation='standard', tz_aware=True)

db = db_client.test
users_collection = db.get_collection('users')
posts_collection = db.get_collection('posts') 


def upload_media_to_s3(file, object_key: str):
    s3_client.upload_fileobj(
        file.file, 
        AWS_BUCKET_NAME, 
        object_key,
        ExtraArgs={"ContentType": file.content_type}
    )


def get_s3_media_url(object_key: str):
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': AWS_BUCKET_NAME, 'Key': object_key},
        ExpiresIn=3600  # URL valid for 1 hour
    )
    return {"download_url": url}