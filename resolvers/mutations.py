from ariadne import MutationType
from db import get_db
from models import Vendor, Product, Log, UserInteraction
from datetime import datetime
import json

mutation = MutationType()

@mutation.field("createVendor")
async def resolve_create_vendor(_, info, username, name, ownerId):
    db = get_db()
    vendor = Vendor(
        username=username,
        name=name,
        owner_id=ownerId,
        account_types=["basic"],
        created_by=ownerId,
        created_at=datetime.utcnow().isoformat(),  # استفاده از UTC
        updated_by=ownerId,
        updated_at=datetime.utcnow().isoformat()  # استفاده از UTC
    )
    result = db.vendors.insert_one(vendor.dict())
    vendor_id = str(result.inserted_id)
    vendor.id = vendor_id

    # ثبت لاگ
    log = Log(
        model_type="Vendor",
        model_id=vendor_id,
        action="create",
        changed_by=ownerId,
        changed_at=datetime.utcnow().isoformat(),  # استفاده از UTC
        new_data=json.dumps(vendor.dict(), ensure_ascii=False)  # پشتیبانی از فارسی
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    # ذخیره id در دیتابیس
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})

    return vendor.__dict__

@mutation.field("createProduct")
async def resolve_create_product(_, info, vendorId, name):
    db = get_db()
    product = Product(
        vendor_id=vendorId,
        names=[name],
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
        category_ids=[],
        subcategory_ids=[],
        created_by=vendorId,
        created_at=datetime.utcnow().isoformat(),  # استفاده از UTC
        updated_by=vendorId,
        updated_at=datetime.utcnow().isoformat()  # استفاده از UTC
    )
    result = db.products.insert_one(product.dict())
    product_id = str(result.inserted_id)
    product.id = product_id

    # ثبت لاگ
    log = Log(
        model_type="Product",
        model_id=product_id,
        action="create",
        changed_by=vendorId,
        changed_at=datetime.utcnow().isoformat(),  # استفاده از UTC
        new_data=json.dumps(product.dict(), ensure_ascii=False)  # پشتیبانی از فارسی
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    # ذخیره id در دیتابیس
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})

    return product.__dict__

@mutation.field("trackInteraction")
async def resolve_track_interaction(_, info, targetType, targetId, action):
    db = get_db()
    interaction = UserInteraction(
        user_id="66f1a2b3c8d9e4f2b8c7d590",
        target_type=targetType,
        target_id=targetId,
        action=action,
        timestamp=datetime.utcnow().isoformat()  # استفاده از UTC
    )
    result = db.user_interactions.insert_one(interaction.dict())
    interaction.id = str(result.inserted_id)
    return interaction.__dict__