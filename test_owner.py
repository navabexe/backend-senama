from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId to fix the error

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "senama_db"
OWNER_ID = "67c1f3c76bbc838b50bc4d91"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

try:
    owner_id_obj = ObjectId(OWNER_ID)
    owner = db.owners.find_one({"_id": owner_id_obj})

    if owner:
        print("Owner found")
        print(owner)
    else:
        print(f"Owner {OWNER_ID} not found.")
except Exception as e:
    print(f"error: {str(e)}")

client.close()