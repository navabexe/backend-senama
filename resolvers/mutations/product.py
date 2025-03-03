from ariadne import MutationType

from db import db
from services.product import create_product
from schemas.product import ProductCreate
from utils import get_current_user

mutation = MutationType()

@mutation.field("createProduct")
async def resolve_create_product(_, info, vendorId, name, categoryIds):
    user_id = get_current_user(info, db)
    product_data = ProductCreate(
        vendor_id=vendorId,
        name=name,
        category_ids=categoryIds
    )
    return create_product(user_id, product_data)