from ariadne import MutationType
from core.auth import get_current_user
from db import get_db
from schemas.product import ProductCreate
from services.product.crud import create_product, update_product, delete_product

mutation = MutationType()


@mutation.field("createProduct")
async def resolve_create_product(_, info, vendorId, name, categoryIds):
    user_id = get_current_user(info, get_db())
    product_data = ProductCreate(
        vendor_id=vendorId,
        name=name,
        category_ids=categoryIds
    )
    return create_product(user_id, product_data)


@mutation.field("updateProduct")
async def resolve_update_product(_, info, productId, name=None, categoryIds=None):
    user_id = get_current_user(info, get_db())
    update_data = {
        "name": name,
        "category_ids": categoryIds
    }
    return update_product(user_id, productId, update_data)


@mutation.field("deleteProduct")
async def resolve_delete_product(_, info, productId):
    user_id = get_current_user(info, get_db())
    return delete_product(user_id, productId)