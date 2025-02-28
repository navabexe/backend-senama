from ariadne import MutationType
from db import get_db
from models.vendor import Vendor
from datetime import datetime, UTC
from bson import ObjectId

from utils import json_serialize

mutation = MutationType()


@mutation.field("createVendor")
async def resolve_create_vendor(_, info, username, name, ownerName, ownerPhone, address, location, city, province,
                                categoryIds):
    db = get_db()
    fake_owner_id = "66f1a2b3c8d9e4f2b8c7d590"  # فعلاً فیک

    # چک کردن وجود دسته‌بندی‌ها
    try:
        category_ids_obj = [ObjectId(cid) for cid in categoryIds]
        for cid in category_ids_obj:
            if not db.categories.find_one({"_id": cid}):
                raise ValueError(f"Category with ID {cid} not found")
    except ValueError as e:
        raise ValueError(f"Invalid categoryIds format or category not found: {str(e)}")

    vendor = Vendor(
        username=username,
        name=name,
        owner_name=ownerName,
        owner_phone=ownerPhone,
        address=address,
        location=location,
        city=city,
        province=province,
        category_ids=categoryIds,  # اجباری کردن category_ids
        created_by=fake_owner_id,
        created_at=datetime.now(UTC).isoformat(),
        updated_by=fake_owner_id,
        updated_at=datetime.now(UTC).isoformat()
    )
    result = db.vendors.insert_one(vendor.dict())
    vendor_id = str(result.inserted_id)
    vendor.id = vendor_id

    from models.log import Log
    log = Log(
        model_type="Vendor",
        model_id=vendor_id,
        action="create",
        changed_by=fake_owner_id,
        changed_at=datetime.now(UTC).isoformat(),
        new_data=json_serialize(vendor.dict())
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})

    vendor_dict = vendor.__dict__
    vendor_dict["id"] = vendor_id
    return vendor_dict


@mutation.field("updateVendor")
async def resolve_update_vendor(_, info, vendorId, name=None, logoUrls=None, bannerUrls=None, bios=None, aboutUs=None,
                                branches=None, businessDetails=None, visibility=None, attachedVendors=None,
                                blockedVendors=None, accountTypes=None, socialLinks=None, messengerLinks=None):
    db = get_db()
    try:
        vendor_id_obj = ObjectId(vendorId)
        vendor = db.vendors.find_one({"_id": vendor_id_obj})
        if not vendor:
            raise ValueError(f"Vendor with ID {vendorId} not found")
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {vendorId}")

    old_data = vendor.copy()
    if name is not None:
        vendor["name"] = name
    if logoUrls is not None:
        vendor["logo_urls"] = logoUrls
    if bannerUrls is not None:
        vendor["banner_urls"] = bannerUrls
    if bios is not None:
        vendor["bios"] = bios
    if aboutUs is not None:
        vendor["about_us"] = aboutUs
    if branches is not None:
        vendor["branches"] = branches
    if businessDetails is not None:
        vendor["business_details"] = businessDetails
    if visibility is not None:
        vendor["visibility"] = visibility
    if attachedVendors is not None:
        vendor["attached_vendors"] = attachedVendors
    if blockedVendors is not None:
        vendor["blocked_vendors"] = blockedVendors
    if accountTypes is not None:
        vendor["account_types"] = accountTypes
    if socialLinks is not None:
        vendor["social_links"] = socialLinks
    if messengerLinks is not None:
        vendor["messenger_links"] = messengerLinks
    vendor["updated_at"] = datetime.now(UTC).isoformat()

    db.vendors.update_one({"_id": vendor_id_obj}, {"$set": vendor})

    from models.log import Log
    log = Log(
        model_type="Vendor",
        model_id=vendorId,
        action="update",
        changed_by=vendor["created_by"],
        changed_at=datetime.now(UTC).isoformat(),
        previous_data=json_serialize(old_data),
        new_data=json_serialize(vendor)
    )
    log_result = db.logs.insert_one(log.dict())
    log.id = str(log_result.inserted_id)
    db.logs.update_one({"_id": log_result.inserted_id}, {"$set": {"id": log.id}})

    vendor["id"] = str(vendor["_id"])
    del vendor["_id"]
    return vendor


@mutation.field("deleteVendor")
async def resolve_delete_vendor(_, info, vendorId):
    db = get_db()
    try:
        vendor_id_obj = ObjectId(vendorId)
        vendor = db.vendors.find_one({"_id": vendor_id_obj})
        if not vendor:
            raise ValueError(f"Vendor with ID {vendorId} not found")
    except ValueError:
        raise ValueError(f"Invalid vendorId format: {vendorId}")

    old_data = vendor.copy()
    db.vendors.delete_one({"_id": vendor_id_obj})
    from models.log import Log
    log = Log(
        model_type="Vendor",
        model_id=vendorId,
        action="delete",
        changed_by=vendor["created_by"],
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