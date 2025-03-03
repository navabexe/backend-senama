import re
from bson import ObjectId
from db import get_db
from utils import get_current_user


async def resolve_my_vendor_profile(_, info):
    """Retrieve the profile of the vendor created by the current user."""
    db = get_db()
    user_id = get_current_user(info, db)
    vendor = db.vendors.find_one({"created_by": user_id})
    if not vendor:
        return None
    vendor["id"] = str(vendor["_id"])
    del vendor["_id"]
    return vendor


async def resolve_vendor_profile(_, info, vendorId):
    """Retrieve the profile of a specific vendor by ID."""
    db = get_db()
    try:
        vendor_id_obj = ObjectId(vendorId)
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {vendorId}")

    vendor = db.vendors.find_one({"_id": vendor_id_obj})
    if not vendor:
        raise ValueError(f"Vendor with ID {vendorId} not found")
    vendor["id"] = str(vendor["_id"])
    del vendor["_id"]
    return vendor


async def resolve_search_vendors(_, info, username=None, name=None, city=None, province=None, businessCategoryId=None):
    """Search vendors based on filters like username, name, city, province, or business category."""
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
    if businessCategoryId:
        try:
            query["business_category_ids"] = ObjectId(businessCategoryId)
        except ValueError:
            raise ValueError(f"Invalid businessCategoryId: {businessCategoryId}")

    vendors = db.vendors.find(query).limit(50)
    return [{"id": str(v["_id"]), **{k: v for k, v in v.items() if k != "_id"}} for v in vendors]