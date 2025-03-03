import re
from bson import ObjectId
from app.exceptions import validation_error, server_error
from db import get_db


async def search_vendors(username=None, name=None, city=None, province=None, business_category_id=None, limit=10,
                         offset=0) -> list:
    db = get_db()
    query = {}
    if username:
        query["username"] = {"$regex": re.escape(username), "$options": "i"}
    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}
    if city:
        query["city"] = city
    if province:
        query["province"] = province
    if business_category_id:
        try:
            query["business_category_ids"] = ObjectId(business_category_id)
        except ValueError:
            raise validation_error("Category ID", f"{business_category_id} has an invalid format")

    try:
        vendors = db.vendors.find(query).skip(offset).limit(limit)
        result = []
        for v in vendors:
            if "_id" not in v or not v["_id"]:
                raise server_error("Vendor without ID found in database")
            v["id"] = str(v["_id"])
            del v["_id"]
            result.append(v)
        return result
    except Exception as e:
        raise server_error(f"Error in searching vendors: {str(e)}")