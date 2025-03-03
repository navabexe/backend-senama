from pymongo import MongoClient
from app.config import config

client = MongoClient(config.MONGO_URI)
db = client.get_default_database()


def get_db():
    return db