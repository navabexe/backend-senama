from ariadne import QueryType
from db import get_db
from bson import ObjectId

query = QueryType()


@query.field("myVendorProfile")
async def resolve_my_vendor_profile(_, info):
    db = get_db()
    vendor = db.vendors.find_one({"username": "sara_mobl_test5"})
    if vendor:
        vendor["id"] = str(vendor["_id"])
        del vendor["_id"]
        owner = db.owners.find_one({"_id": ObjectId(vendor["owner_id"])})
        if owner:
            owner["id"] = str(owner["_id"])
            del owner["_id"]
            vendor["owner"] = owner
        return vendor
    return None


@query.field("vendorProfile")
async def resolve_vendor_profile(_, info, vendorId):
    db = get_db()
    try:
        vendor_id_obj = ObjectId(vendorId)
        vendor = db.vendors.find_one({"_id": vendor_id_obj})
        if not vendor:
            return None
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {vendorId}")

    vendor["id"] = str(vendor["_id"])
    del vendor["_id"]
    owner = db.owners.find_one({"_id": ObjectId(vendor["owner_id"])})
    if owner:
        owner["id"] = str(owner["_id"])
        del owner["_id"]
        vendor["owner"] = owner
    return vendor


@query.field("searchVendors")
async def resolve_search_vendors(_, info, username=None):
    db = get_db()
    query = {}
    if username:
        query["username"] = {"$regex": username, "$options": "i"}
    vendors = db.vendors.find(query)
    result = []
    for vendor in vendors:
        vendor["id"] = str(vendor["_id"])
        del vendor["_id"]
        owner = db.owners.find_one({"_id": ObjectId(vendor["owner_id"])})
        if owner:
            owner["id"] = str(owner["_id"])
            del owner["_id"]
            vendor["owner"] = owner
        result.append(vendor)
    return result