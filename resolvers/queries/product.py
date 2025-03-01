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
        return [
            {
                "id": str(p["_id"]),
                "vendor_id": p["vendor_id"],
                "names": p["names"],
                "short_descriptions": p["short_descriptions"],
                "prices": p["prices"],
                "colors": p["colors"],
                "images": p["images"],
                "video_urls": p["video_urls"],
                "audio_files": p["audio_files"],
                "technical_specs": p["technical_specs"],
                "tags": p["tags"],
                "thumbnail_urls": p["thumbnail_urls"],
                "suggested_products": p["suggested_products"],
                "status": p["status"],
                "qr_code_url": p["qr_code_url"],
                "category_ids": p["category_ids"],
                "subcategory_ids": p["subcategory_ids"],
                "created_by": p["created_by"],
                "created_at": p["created_at"],
                "updated_by": p["updated_by"],
                "updated_at": p["updated_at"]
            } for p in products
        ]
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {vendorId}")


@query.field("searchProducts")
async def resolve_search_products(_, info, name=None, tag=None, categoryId=None, status=None):
    db = get_db()
    query = {}
    if name:
        query["names"] = {"$regex": name, "$options": "i"}
    if tag:
        query["tags"] = tag
    if categoryId:
        query["category_ids"] = categoryId
    if status:
        query["status"] = status

    products = list(db.products.find(query))
    if not products:
        return []
    return [
        {
            "id": str(p["_id"]),
            "vendor_id": p["vendor_id"],
            "names": p["names"],
            "short_descriptions": p["short_descriptions"],
            "prices": p["prices"],
            "colors": p["colors"],
            "images": p["images"],
            "video_urls": p["video_urls"],
            "audio_files": p["audio_files"],
            "technical_specs": p["technical_specs"],
            "tags": p["tags"],
            "thumbnail_urls": p["thumbnail_urls"],
            "suggested_products": p["suggested_products"],
            "status": p["status"],
            "qr_code_url": p["qr_code_url"],
            "category_ids": p["category_ids"],
            "subcategory_ids": p["subcategory_ids"],
            "created_by": p["created_by"],
            "created_at": p["created_at"],
            "updated_by": p["updated_by"],
            "updated_at": p["updated_at"]
        } for p in products
    ]