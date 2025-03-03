from bson import ObjectId
from db import get_db


async def resolve_products(_, info, vendorId):
    db = get_db()
    try:
        vendor_id_obj = ObjectId(vendorId)
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {vendorId}")

    products = db.products.find({"vendor_id": vendorId}).limit(50)
    return [{"id": str(p["_id"]), **{k: v for k, v in p.items() if k != "_id"}} for p in products]