from ariadne import QueryType
from db import get_db

query = QueryType()

@query.field("myVendorProfile")
async def resolve_my_vendor_profile(_, info):
    db = get_db()
    vendor = db.vendors.find_one({"username": "sara_mobl_test5"})
    if vendor:
        vendor["id"] = str(vendor["_id"])
        del vendor["_id"]
        return vendor
    return None

@query.field("vendorProfile")
async def resolve_vendor_profile(_, info, vendorId):
    db = get_db()
    vendor = db.vendors.find_one({"_id": vendorId})
    if vendor:
        vendor["id"] = str(vendor["_id"])
        del vendor["_id"]
        return vendor
    return None

@query.field("products")
async def resolve_products(_, info, vendorId):
    db = get_db()
    products = db.products.find({"vendor_id": vendorId})
    return [{"id": str(p["_id"]), **{k: v for k, v in p.items() if k != "_id"}} for p in products]

@query.field("logs")
async def resolve_logs(_, info, modelType, modelId):
    db = get_db()
    # فقط لاگ‌هایی که id دارند و null نیستند را برگردانید
    logs = list(db.logs.find({
        "model_type": modelType,
        "model_id": modelId,
        "id": {"$exists": True, "$ne": None}
    }))
    # تبدیل _id به id در صورت نیاز و پردازش داده‌ها
    for log in logs:
        log["id"] = str(log["_id"]) if "_id" in log else log["id"]
        if "previous_data" in log and log["previous_data"] is None:
            log["previous_data"] = ""  # جایگزینی null با مقدار پیش‌فرض
    return logs

@query.field("interactions")
async def resolve_interactions(_, info, userId):
    db = get_db()
    interactions = db.user_interactions.find({"user_id": userId})
    return [{"id": str(i["_id"]), **{k: v for k, v in i.items() if k != "_id"}} for i in interactions]