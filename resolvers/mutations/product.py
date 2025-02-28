from ariadne import MutationType
from db import get_db
from models.product import Product
from datetime import datetime, UTC
from bson import ObjectId

from utils import json_serialize

mutation = MutationType()


@mutation.field("createProduct")
async def resolve_create_product(_, info, vendorId, name, categoryIds):
    db = get_db()
    try:
        vendor_id_obj = ObjectId(vendorId)
        vendor = db.vendors.find_one({"_id": vendor_id_obj})
        if not vendor:
            raise ValueError(f"Vendor with ID {vendorId} not found")
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {vendorId}")

    # چک کردن وجود دسته‌بندی‌ها
    try:
        category_ids_obj = [ObjectId(cid) for cid in categoryIds]
        for cid in category_ids_obj:
            if not db.categories.find_one({"_id": cid}):
                raise ValueError(f"Category with ID {cid} not found")
    except ValueError as e:
        raise ValueError(f"Invalid categoryIds format or category not found: {str(e)}")

    product = Product(
        vendor_id=vendorId,
        names=[name],  # تغییر name به names
        short_descriptions=[],
        prices=[],
        colors=[],
        images=[],
        video_urls=[],
        audio_files=[],
        technical_specs=[],
        tags=[],
        thumbnail_urls=[],
        suggested_products=[],
        status="draft",
        qr_code_url=f"https://example.com/product/{vendorId}/{name}/qr",
        category_ids=categoryIds,  # اجباری کردن category_ids
        subcategory_ids=[],
        created_by=vendorId,
        created_at=datetime.now(UTC).isoformat(),
        updated_by=vendorId,
        updated_at=datetime.now(UTC).isoformat()
    )
    result = db.products.insert_one(product.dict())
    product_id = str(result.inserted_id)
    product.id = product_id
    from models.log import Log
    log = Log(
        model_type="Product",
        model_id=product_id,
        action="create",
        changed_by=vendorId,
        changed_at=datetime.now(UTC).isoformat(),
        new_data=json_serialize(product.dict())
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})
    product_dict = product.__dict__
    product_dict["id"] = product_id
    return product_dict


@mutation.field("updateProduct")
async def resolve_update_product(_, info, productId, name=None, shortDescriptions=None, prices=None, colors=None,
                                 images=None, videoUrls=None, audioFiles=None, technicalSpecs=None, tags=None,
                                 thumbnailUrls=None, suggestedProducts=None, status=None, qrCodeUrl=None,
                                 categoryIds=None, subcategoryIds=None):
    db = get_db()
    try:
        product_id_obj = ObjectId(productId)
        product = db.products.find_one({"_id": product_id_obj})
        if not product:
            raise ValueError(f"Product with ID {productId} not found")
    except ValueError:
        raise ValueError(f"Invalid productId format: {productId}")

    old_data = product.copy()
    if name is not None:
        product["names"] = [name]  # تغییر name به names
    if shortDescriptions is not None:
        product["short_descriptions"] = shortDescriptions
    if prices is not None:
        product["prices"] = prices
    if colors is not None:
        product["colors"] = colors
    if images is not None:
        product["images"] = images
    if videoUrls is not None:
        product["video_urls"] = videoUrls
    if audioFiles is not None:
        product["audio_files"] = audioFiles
    if technicalSpecs is not None:
        product["technical_specs"] = technicalSpecs
    if tags is not None:
        product["tags"] = tags
    if thumbnailUrls is not None:
        product["thumbnail_urls"] = thumbnailUrls
    if suggestedProducts is not None:
        product["suggested_products"] = suggestedProducts
    if status is not None:
        product["status"] = status
    if qrCodeUrl is not None:
        product["qr_code_url"] = qrCodeUrl
    if categoryIds is not None:
        product["category_ids"] = categoryIds
    if subcategoryIds is not None:
        product["subcategory_ids"] = subcategoryIds
    product["updated_at"] = datetime.now(UTC).isoformat()

    db.products.update_one({"_id": product_id_obj}, {"$set": product})
    from models.log import Log
    log = Log(
        model_type="Product",
        model_id=productId,
        action="update",
        changed_by=product["created_by"],
        changed_at=datetime.now(UTC).isoformat(),
        previous_data=json_serialize(old_data),
        new_data=json_serialize(product)
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})
    product["id"] = str(product["_id"])
    del product["_id"]
    return product


@mutation.field("deleteProduct")
async def resolve_delete_product(_, info, productId):
    db = get_db()
    try:
        product_id_obj = ObjectId(productId)
        product = db.products.find_one({"_id": product_id_obj})
        if not product:
            raise ValueError(f"Product with ID {productId} not found")
    except ValueError:
        raise ValueError(f"Invalid productId format: {productId}")

    old_data = product.copy()
    db.products.delete_one({"_id": product_id_obj})
    from models.log import Log
    log = Log(
        model_type="Product",
        model_id=productId,
        action="delete",
        changed_by=product["created_by"],
        changed_at=datetime.now(UTC).isoformat(),
        previous_data=json_serialize(old_data),
        new_data=""
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})
    old_data["id"] = str(old_data["_id"])
    del old_data["_id"]
    return old_data