import re
from datetime import datetime, UTC
from bson import ObjectId
from app.exceptions import validation_error, not_found_error, server_error, CustomAPIError
from db import get_db
from models import Vendor
from schemas.vendor import VendorCreate, VendorResponse


def create_vendor(user_id: str, vendor_data: VendorCreate) -> VendorResponse:
    db = get_db()
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if "vendor" not in user["roles"]:
            raise validation_error("User role", "User must have vendor role")

        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", vendor_data.username):
            raise validation_error("Username", "Must be 3-20 characters and only include letters, numbers, or _")
        if db.vendors.find_one({"username": vendor_data.username}):
            raise validation_error("Username", f"{vendor_data.username} is already registered")

        if not vendor_data.business_category_ids:
            raise validation_error("Business category", "At least one category must be selected")

        business_category_ids_obj = []
        for cid in vendor_data.business_category_ids:
            try:
                cid_obj = ObjectId(cid)
                if not db.business_categories.find_one({"_id": cid_obj}):
                    raise not_found_error("Category", cid)
                business_category_ids_obj.append(cid)
            except ValueError:
                raise validation_error("Category ID", f"{cid} has an invalid format")

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
            created_at=datetime.now(UTC).isoformat(),
            updated_by=user_id,
            updated_at=datetime.now(UTC).isoformat()
        )
        result = db.vendors.insert_one(vendor.dict())
        vendor_id = str(result.inserted_id)
        vendor.id = vendor_id
        return VendorResponse(**vendor.dict())
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in creating vendor: {str(e)}")
        raise


def update_vendor(user_id: str, vendor_id: str, update_data: dict) -> VendorResponse:
    db = get_db()
    try:
        try:
            vendor_id_obj = ObjectId(vendor_id)
        except ValueError:
            raise validation_error("Vendor ID", "Invalid format")

        vendor = db.vendors.find_one({"_id": vendor_id_obj})
        if not vendor:
            raise not_found_error("Vendor", vendor_id)
        if vendor["created_by"] != user_id:
            raise validation_error("Permission", "You do not have permission to update this vendor")

        update_fields = {k: v for k, v in update_data.items() if v is not None}
        if "business_category_ids" in update_fields:
            business_category_ids_obj = []
            for cid in update_fields["business_category_ids"]:
                try:
                    cid_obj = ObjectId(cid)
                    if not db.business_categories.find_one({"_id": cid_obj}):
                        raise not_found_error("Category", cid)
                    business_category_ids_obj.append(cid)
                except ValueError:
                    raise validation_error("Category ID", f"{cid} has an invalid format")
            update_fields["business_category_ids"] = business_category_ids_obj

        update_fields["updated_at"] = datetime.now(UTC).isoformat()
        update_fields["updated_by"] = user_id
        db.vendors.update_one({"_id": vendor_id_obj}, {"$set": update_fields})

        updated_vendor = db.vendors.find_one({"_id": vendor_id_obj})
        return VendorResponse(**updated_vendor)
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in updating vendor: {str(e)}")
        raise


def delete_vendor(user_id: str, vendor_id: str) -> VendorResponse:
    db = get_db()
    try:
        try:
            vendor_id_obj = ObjectId(vendor_id)
        except ValueError:
            raise validation_error("Vendor ID", "Invalid format")

        vendor = db.vendors.find_one({"_id": vendor_id_obj})
        if not vendor:
            raise not_found_error("Vendor", vendor_id)
        if vendor["created_by"] != user_id:
            raise validation_error("Permission", "You do not have permission to delete this vendor")

        db.vendors.delete_one({"_id": vendor_id_obj})
        return VendorResponse(**vendor)
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in deleting vendor: {str(e)}")
        raise


def activate_vendor(admin_id: str, vendor_id: str, vendor_type: str = "basic") -> dict:
    db = get_db()
    try:
        admin = db.users.find_one({"_id": ObjectId(admin_id)})
        if "admin" not in admin["roles"]:
            raise validation_error("User role", "Only admin can activate a vendor")

        try:
            vendor_id_obj = ObjectId(vendor_id)
        except ValueError:
            raise validation_error("Vendor ID", "Invalid format")

        vendor = db.vendors.find_one({"_id": vendor_id_obj})
        if not vendor:
            raise not_found_error("Vendor", vendor_id)

        db.vendors.update_one(
            {"_id": vendor_id_obj},
            {"$set": {"status": "active", "vendor_type": vendor_type, "updated_at": datetime.now(UTC).isoformat(),
                      "updated_by": admin_id}}
        )
        return {"message": f"Vendor {vendor_id} activated with type {vendor_type}"}
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in activating vendor: {str(e)}")
        raise