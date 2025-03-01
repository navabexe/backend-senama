from ariadne import MutationType
from db import get_db
from models.business_category import BusinessCategory
from datetime import datetime, UTC
from bson import ObjectId
from utils import json_serialize

mutation = MutationType()

@mutation.field("createBusinessCategory")
async def resolve_create_business_category(_, info, name):
    db = get_db()
    category = BusinessCategory(
        name=name,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    result = db.business_categories.insert_one(category.dict())
    category_id = str(result.inserted_id)
    category.id = category_id
    return category.__dict__