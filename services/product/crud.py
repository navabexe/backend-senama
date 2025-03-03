from datetime import datetime, UTC
from bson import ObjectId
from app.exceptions import validation_error, not_found_error, server_error, CustomAPIError
from db import get_db
from models import Product
from schemas.product import ProductCreate, ProductResponse


def create_product(user_id: str, product_data: ProductCreate) -> ProductResponse:
    db = get_db()
    try:
        try:
            vendor_id_obj = ObjectId(product_data.vendor_id)
        except ValueError:
            raise validation_error("Vendor ID", "Invalid format")

        vendor = db.vendors.find_one({"_id": vendor_id_obj})
        if not vendor:
            raise not_found_error("Vendor", product_data.vendor_id)
        if vendor["created_by"] != user_id:
            raise validation_error("Permission", "You do not have permission to create a product for this vendor")

        if not product_data.name or len(product_data.name.strip()) < 3:
            raise validation_error("Product name", "Must be at least 3 characters")

        if not product_data.category_ids:
            raise validation_error("Category", "At least one category must be selected")

        category_ids_obj = []
        for cid in product_data.category_ids:
            try:
                cid_obj = ObjectId(cid)
                if not db.business_categories.find_one({"_id": cid_obj}):
                    raise not_found_error("Category", cid)
                category_ids_obj.append(cid)
            except ValueError:
                raise validation_error("Category ID", f"{cid} has an invalid format")

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
            created_at=datetime.now(UTC).isoformat(),
            updated_by=user_id,
            updated_at=datetime.now(UTC).isoformat()
        )
        result = db.products.insert_one(product.dict())
        product_id = str(result.inserted_id)
        product.id = product_id
        return ProductResponse(**product.dict())
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in creating product: {str(e)}")
        raise


def update_product(user_id: str, product_id: str, update_data: dict) -> ProductResponse:
    db = get_db()
    try:
        try:
            product_id_obj = ObjectId(product_id)
        except ValueError:
            raise validation_error("Product ID", "Invalid format")

        product = db.products.find_one({"_id": product_id_obj})
        if not product:
            raise not_found_error("Product", product_id)
        vendor = db.vendors.find_one({"_id": ObjectId(product["vendor_id"])})
        if vendor["created_by"] != user_id:
            raise validation_error("Permission", "You do not have permission to update this product")

        update_fields = {k: v for k, v in update_data.items() if v is not None}
        if "category_ids" in update_fields:
            category_ids_obj = []
            for cid in update_fields["category_ids"]:
                try:
                    cid_obj = ObjectId(cid)
                    if not db.business_categories.find_one({"_id": cid_obj}):
                        raise not_found_error("Category", cid)
                    category_ids_obj.append(cid)
                except ValueError:
                    raise validation_error("Category ID", f"{cid} has an invalid format")
            update_fields["category_ids"] = category_ids_obj

        update_fields["updated_at"] = datetime.now(UTC).isoformat()
        update_fields["updated_by"] = user_id
        db.products.update_one({"_id": product_id_obj}, {"$set": update_fields})

        updated_product = db.products.find_one({"_id": product_id_obj})
        return ProductResponse(**updated_product)
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in updating product: {str(e)}")
        raise


def delete_product(user_id: str, product_id: str) -> ProductResponse:
    db = get_db()
    try:
        try:
            product_id_obj = ObjectId(product_id)
        except ValueError:
            raise validation_error("Product ID", "Invalid format")

        product = db.products.find_one({"_id": product_id_obj})
        if not product:
            raise not_found_error("Product", product_id)
        vendor = db.vendors.find_one({"_id": ObjectId(product["vendor_id"])})
        if vendor["created_by"] != user_id:
            raise validation_error("Permission", "You do not have permission to delete this product")

        db.products.delete_one({"_id": product_id_obj})
        return ProductResponse(**product)
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in deleting product: {str(e)}")
        raise