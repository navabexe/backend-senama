from bson import ObjectId
from core.auth import get_current_user
from db import get_db
from services.vendor.search import search_vendors
from app.exceptions import CustomAPIError


async def resolve_my_vendor_profile(_, info):
    db = get_db()
    user_id = get_current_user(info, db)
    vendor = db.vendors.find_one({"created_by": user_id})
    if not vendor:
        return None
    vendor["id"] = str(vendor["_id"])
    del vendor["_id"]
    return vendor


async def resolve_vendor_profile(_, info, vendorId):
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


async def resolve_search_vendors(_, info, username=None, name=None, city=None, province=None, businessCategoryId=None, limit=10, offset=0):
    try:
        result = await search_vendors(username, name, city, province, businessCategoryId, limit, offset)
        if result is None:
            return []
        return result
    except CustomAPIError as e:
        raise
    except Exception as e:
        raise Exception(f"Unexpected error in vendor search: {str(e)}")