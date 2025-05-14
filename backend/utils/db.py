import os
import pymongo
from dotenv import load_dotenv
import logging
from pymongo.errors import CollectionInvalid

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = pymongo.MongoClient(MONGO_URI)
db = client.users

try:
    user_collection = db.create_collection("users")
except CollectionInvalid:
    user_collection = db.users
