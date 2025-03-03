from ariadne import MutationType
from db import get_db
from models.vendor import Vendor
from datetime import datetime, UTC
from bson import ObjectId
from utils import json_serialize, get_current_user

mutation = MutationType()


@mutation.field("createVendor")
async def resolve_create_vendor(_, info, username, name, ownerName, ownerPhone, address, location, city, province,
                                businessCategoryIds):
    db = get_db()
    user_id = get_current_user(info, db)
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if "vendor" not in user["roles"]:
        raise ValueError("User must have vendor role")  # فقط نقش رو چک می‌کنیم

    if db.vendors.find_one({"username": username}):
        raise ValueError(f"Username {username} already exists")

    try:
        business_category_ids_obj = [ObjectId(cid) for cid in businessCategoryIds]
        for cid in business_category_ids_obj:
            if not db.business_categories.find_one({"_id": cid}):
                raise ValueError(f"Business Category with ID {cid} not found")
    except ValueError as e:
        raise ValueError(f"Invalid businessCategoryIds: {str(e)}")

    vendor = Vendor(
        username=username,
        name=name,
        owner_name=ownerName,
        owner_phone=ownerPhone,
        address=address,
        location=location,
        city=city,
        province=province,
        business_category_ids=businessCategoryIds,
        visibility=True,
        account_types=["free"],
        status="pending",  # وندور در حالت انتظار
        vendor_type="basic",
        created_by=user_id,
        created_at=datetime.now(UTC).isoformat(),
        updated_by=user_id,
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
        changed_by=user_id,
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
    user_id = get_current_user(info, db)

    try:
        vendor_id_obj = ObjectId(vendorId)
        vendor = db.vendors.find_one({"_id": vendor_id_obj})
        if not vendor:
            raise ValueError(f"Vendor with ID {vendorId} not found")
        if vendor["created_by"] != user_id:
            raise ValueError("You are not authorized to update this vendor")
    except ValueError as e:
        raise ValueError(str(e))

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
    vendor["updated_by"] = user_id

    db.vendors.update_one({"_id": vendor_id_obj}, {"$set": vendor})

    from models.log import Log
    log = Log(
        model_type="Vendor",
        model_id=vendorId,
        action="update",
        changed_by=user_id,
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
    user_id = get_current_user(info, db)

    try:
        vendor_id_obj = ObjectId(vendorId)
        vendor = db.vendors.find_one({"_id": vendor_id_obj})
        if not vendor:
            raise ValueError(f"Vendor with ID {vendorId} not found")
        if vendor["created_by"] != user_id:
            raise ValueError("You are not authorized to delete this vendor")
    except ValueError as e:
        raise ValueError(str(e))

    old_data = vendor.copy()
    db.products.delete_many({"vendor_id": vendorId})
    db.stories.delete_many({"vendor_id": vendorId})
    db.follow_blocks.delete_many({"$or": [
        {"follower_id": vendorId},
        {"following_id": vendorId}
    ]})
    db.vendors.delete_one({"_id": vendor_id_obj})

    from models.log import Log
    log = Log(
        model_type="Vendor",
        model_id=vendorId,
        action="delete",
        changed_by=user_id,
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


@mutation.field("activateVendor")
async def resolve_activate_vendor(_, info, vendorId, vendorType="basic"):
    print("Entering activateVendor")  # دیباگ اولیه
    db = get_db()
    try:
        request = info.context.get("request")
        print(f"Request headers: {request.headers}")  # دیباگ هدرها
        admin_id = get_current_user(info, db)
        print(f"Admin ID: {admin_id}")
        admin = db.users.find_one({"_id": ObjectId(admin_id)})
        print(f"Admin: {admin}")
        if not admin or "admin" not in admin["roles"]:
            raise ValueError("Only admins can activate vendors")

        vendor = db.vendors.find_one({"_id": ObjectId(vendorId)})
        print(f"Vendor: {vendor}")
        if not vendor:
            raise ValueError(f"Vendor with ID {vendorId} not found")

        update_result = db.vendors.update_one(
            {"_id": ObjectId(vendorId)},
            {"$set": {"status": "active", "vendor_type": vendorType}}
        )
        print(f"Update result: {update_result.modified_count}")
        return {"message": f"Vendor {vendorId} activated with type {vendorType}"}
    except Exception as e:
        print(f"Error in activateVendor: {str(e)}")
        raise ValueError(f"Failed to activate vendor: {str(e)}")