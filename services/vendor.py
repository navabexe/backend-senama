import re
from datetime import datetime, UTC
from bson import ObjectId
from db import get_db
from models.vendor import Vendor
from schemas.vendor import VendorCreate, VendorResponse
from utils import get_current_user


def create_vendor(user_id: str, vendor_data: VendorCreate) -> VendorResponse:
    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if "vendor" not in user["roles"]:
        raise ValueError("User must have vendor role")

    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", vendor_data.username):
        raise ValueError("Username must be 3-20 characters and contain only letters, numbers, or underscores")
    if db.vendors.find_one({"username": vendor_data.username}):
        raise ValueError(f"Username {vendor_data.username} already exists")

    try:
        business_category_ids_obj = [ObjectId(cid) for cid in vendor_data.business_category_ids]
        for cid in business_category_ids_obj:
            if not db.business_categories.find_one({"_id": cid}):
                raise ValueError(f"Business Category with ID {cid} not found")
    except ValueError as e:
        raise ValueError(f"Invalid businessCategoryIds: {str(e)}")

    vendor = Vendor(
        username=vendor_data.username,
        name=vendor_data.name,
        owner_name=vendor_data.owner_name,
        owner_phone=vendor_data.owner_phone,
        address=vendor_data.address,
        location=vendor_data.location,
        city=vendor_data.city,
        province=vendor_data.province,
        business_category_ids=vendor_data.business_category_ids,
        visibility=True,
        account_types=["free"],
        status="pending",
        vendor_type="basic",
        created_by=user_id,
        created_at=datetime.now(UTC),
        updated_by=user_id,
        updated_at=datetime.now(UTC)
    )
    result = db.vendors.insert_one(vendor.dict())
    vendor_id = str(result.inserted_id)
    vendor.id = vendor_id
    return VendorResponse(**vendor.dict())


def update_vendor(user_id: str, vendor_id: str, update_data: dict) -> VendorResponse:
    db = get_db()
    try:
        vendor_id_obj = ObjectId(vendor_id)
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {vendor_id}")

    vendor = db.vendors.find_one({"_id": vendor_id_obj})
    if not vendor:
        raise ValueError(f"Vendor with ID {vendor_id} not found")
    if vendor["created_by"] != user_id:
        raise ValueError("You are not authorized to update this vendor")

    update_fields = {k: v for k, v in update_data.items() if v is not None}
    if "business_category_ids" in update_fields:
        try:
            update_fields["business_category_ids"] = [ObjectId(cid) for cid in update_fields["business_category_ids"]]
            for cid in update_fields["business_category_ids"]:
                if not db.business_categories.find_one({"_id": cid}):
                    raise ValueError(f"Business Category with ID {cid} not found")
        except ValueError as e:
            raise ValueError(f"Invalid businessCategoryIds: {str(e)}")

    update_fields["updated_at"] = datetime.now(UTC)
    update_fields["updated_by"] = user_id
    db.vendors.update_one({"_id": vendor_id_obj}, {"$set": update_fields})

    updated_vendor = db.vendors.find_one({"_id": vendor_id_obj})
    return VendorResponse(**updated_vendor)


def delete_vendor(user_id: str, vendor_id: str) -> VendorResponse:
    db = get_db()
    try:
        vendor_id_obj = ObjectId(vendor_id)
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {vendor_id}")

    vendor = db.vendors.find_one({"_id": vendor_id_obj})
    if not vendor:
        raise ValueError(f"Vendor with ID {vendor_id} not found")
    if vendor["created_by"] != user_id:
        raise ValueError("You are not authorized to delete this vendor")

    db.vendors.delete_one({"_id": vendor_id_obj})
    return VendorResponse(**vendor)


def activate_vendor(admin_id: str, vendor_id: str, vendor_type: str = "basic") -> dict:
    db = get_db()
    admin = db.users.find_one({"_id": ObjectId(admin_id)})
    if "admin" not in admin["roles"]:
        raise ValueError("Only admins can activate vendors")

    try:
        vendor_id_obj = ObjectId(vendor_id)
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {vendor_id}")

    vendor = db.vendors.find_one({"_id": vendor_id_obj})
    if not vendor:
        raise ValueError(f"Vendor with ID {vendor_id} not found")

    db.vendors.update_one(
        {"_id": vendor_id_obj},
        {"$set": {"status": "active", "vendor_type": vendor_type, "updated_at": datetime.now(UTC),
                  "updated_by": admin_id}}
    )
    return {"message": f"Vendor {vendor_id} activated with type {vendor_type}"}