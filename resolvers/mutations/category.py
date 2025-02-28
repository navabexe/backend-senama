from ariadne import MutationType
from db import get_db
from models.category import Category, Subcategory
from datetime import datetime, UTC
from bson import ObjectId

mutation = MutationType()


@mutation.field("createCategory")
async def resolve_create_category(_, info, name):
    db = get_db()
    category = Category(
        name=name,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    result = db.categories.insert_one(category.dict())
    category_id = str(result.inserted_id)
    category.id = category_id
    return category.__dict__


@mutation.field("createSubcategory")
async def resolve_create_subcategory(_, info, categoryId, name):
    db = get_db()
    try:
        category_id_obj = ObjectId(categoryId)
        if not db.categories.find_one({"_id": category_id_obj}):
            raise ValueError(f"Category with ID {categoryId} not found")
    except ValueError:
        raise ValueError(f"Invalid categoryId format: {categoryId}")

    subcategory = Subcategory(
        category_id=categoryId,
        name=name,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    result = db.subcategories.insert_one(subcategory.dict())
    subcategory_id = str(result.inserted_id)
    subcategory.id = subcategory_id
    return subcategory.__dict__