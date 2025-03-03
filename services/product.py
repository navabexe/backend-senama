from datetime import datetime, UTC
from bson import ObjectId
from db import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductResponse
from utils import get_current_user


def create_product(user_id: str, product_data: ProductCreate) -> ProductResponse:
    db = get_db()
    try:
        vendor_id_obj = ObjectId(product_data.vendor_id)
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {product_data.vendor_id}")

    vendor = db.vendors.find_one({"_id": vendor_id_obj})
    if not vendor:
        raise ValueError(f"Vendor with ID {product_data.vendor_id} not found")
    if vendor["created_by"] != user_id:
        raise ValueError("You are not authorized to create products for this vendor")

    try:
        category_ids_obj = [ObjectId(cid) for cid in product_data.category_ids]
        for cid in category_ids_obj:
            if not db.categories.find_one({"_id": cid}):
                raise ValueError(f"Category with ID {cid} not found")
    except ValueError as e:
        raise ValueError(f"Invalid categoryIds format or category not found: {str(e)}")

    product = Product(
        vendor_id=product_data.vendor_id,
        names=[product_data.name],
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
        qr_code_url=None,
        category_ids=product_data.category_ids,
        subcategory_ids=[],
        created_by=user_id,
        created_at=datetime.now(UTC),
        updated_by=user_id,
        updated_at=datetime.now(UTC)
    )
    result = db.products.insert_one(product.dict())
    product_id = str(result.inserted_id)
    product.id = product_id
    return ProductResponse(**product.dict())