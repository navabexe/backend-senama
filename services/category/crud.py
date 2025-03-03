from datetime import datetime, UTC
from bson import ObjectId
from app.exceptions import validation_error, not_found_error, server_error, CustomAPIError
from db import get_db
from models import Category
from schemas.category import CategoryCreate, CategoryResponse


async def create_category(user_id: str, category_data: CategoryCreate) -> CategoryResponse:
    db = get_db()
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user or "admin" not in user.get("roles", []):
            raise validation_error("User role", "Only admin can create a category")

        if not category_data.name or len(category_data.name.strip()) < 3:
            raise validation_error("Category name", "Must be at least 3 characters")
        if db.business_categories.find_one({"name": category_data.name}):
            raise validation_error("Category name", f"{category_data.name} is already registered")

        category = Category(
            name=category_data.name,
            description=category_data.description,
            created_by=user_id,
            created_at=datetime.now(UTC).isoformat(),
            updated_by=user_id,
            updated_at=datetime.now(UTC).isoformat()
        )
        result = db.business_categories.insert_one(category.dict())
        category_id = str(result.inserted_id)
        category.id = category_id
        return CategoryResponse(**category.dict())
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in creating category: {str(e)}")
        raise


def update_category(user_id: str, category_id: str, update_data: dict) -> CategoryResponse:
    db = get_db()
    try:
        try:
            category_id_obj = ObjectId(category_id)
        except ValueError:
            raise validation_error("Category ID", "Invalid format")

        category = db.business_categories.find_one({"_id": category_id_obj})
        if not category:
            raise not_found_error("Category", category_id)
        if category["created_by"] != user_id:
            raise validation_error("Permission", "You do not have permission to update this category")

        update_fields = {k: v for k, v in update_data.items() if v is not None}
        if "name" in update_fields and db.business_categories.find_one(
                {"name": update_fields["name"], "_id": {"$ne": category_id_obj}}):
            raise validation_error("Category name", f"{update_fields['name']} is already registered")

        update_fields["updated_at"] = datetime.now(UTC).isoformat()
        update_fields["updated_by"] = user_id
        db.business_categories.update_one({"_id": category_id_obj}, {"$set": update_fields})

        updated_category = db.business_categories.find_one({"_id": category_id_obj})
        return CategoryResponse(**updated_category)
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in updating category: {str(e)}")
        raise


def delete_category(user_id: str, category_id: str) -> CategoryResponse:
    db = get_db()
    try:
        try:
            category_id_obj = ObjectId(category_id)
        except ValueError:
            raise validation_error("Category ID", "Invalid format")

        category = db.business_categories.find_one({"_id": category_id_obj})
        if not category:
            raise not_found_error("Category", category_id)
        if category["created_by"] != user_id:
            raise validation_error("Permission", "You do not have permission to delete this category")

        db.business_categories.delete_one({"_id": category_id_obj})
        return CategoryResponse(**category)
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in deleting category: {str(e)}")
        raise