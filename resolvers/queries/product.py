from ariadne import QueryType
from db import get_db
from bson import ObjectId

query = QueryType()

@query.field("products")
async def resolve_products(_, info, vendorId):
    db = get_db()
    try:
        vendor_id_obj = ObjectId(vendorId)
        products = db.products.find({"vendor_id": vendorId})
        return [{"id": str(p["_id"]), **{k: v for k, v in p.items() if k != "_id"}} for p in products]
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {vendorId}")

@query.field("searchProducts")
async def resolve_search_products(_, info, name=None):
    db = get_db()
    query = {}
    if name:
        query["names"] = {"$regex": name, "$options": "i"}
    products = db.products.find(query)
    return [{"id": str(p["_id"]), **{k: v for k, v in p.items() if k != "_id"}} for p in products]