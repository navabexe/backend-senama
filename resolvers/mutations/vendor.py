from ariadne import MutationType
from services.vendor import create_vendor, update_vendor, delete_vendor, activate_vendor
from schemas.vendor import VendorCreate
from utils import get_current_user
from db import get_db

mutation = MutationType()

@mutation.field("createVendor")
async def resolve_create_vendor(_, info, username, name, ownerName, ownerPhone, address, location, city, province, businessCategoryIds):
    user_id = get_current_user(info, get_db())
    vendor_data = VendorCreate(
        username=username,
        name=name,
        owner_name=ownerName,
        owner_phone=ownerPhone,
        address=address,
        location=location,
        city=city,
        province=province,
        business_category_ids=businessCategoryIds
    )
    return create_vendor(user_id, vendor_data)

@mutation.field("updateVendor")
async def resolve_update_vendor(_, info, vendorId, name=None, logoUrls=None, bannerUrls=None, bios=None, aboutUs=None,
                                branches=None, businessDetails=None, visibility=None, attachedVendors=None,
                                blockedVendors=None, accountTypes=None, socialLinks=None, messengerLinks=None):
    user_id = get_current_user(info, get_db())
    update_data = {
        "name": name,
        "logo_urls": logoUrls,
        "banner_urls": bannerUrls,
        "bios": bios,
        "about_us": aboutUs,
        "branches": branches,
        "business_details": businessDetails,
        "visibility": visibility,
        "attached_vendors": attachedVendors,
        "blocked_vendors": blockedVendors,
        "account_types": accountTypes,
        "social_links": socialLinks,
        "messenger_links": messengerLinks
    }
    return update_vendor(user_id, vendorId, update_data)

@mutation.field("deleteVendor")
async def resolve_delete_vendor(_, info, vendorId):
    user_id = get_current_user(info, get_db())
    return delete_vendor(user_id, vendorId)

@mutation.field("activateVendor")
async def resolve_activate_vendor(_, info, vendorId, vendorType="basic"):
    admin_id = get_current_user(info, get_db())
    return activate_vendor(admin_id, vendorId, vendorType)