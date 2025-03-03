from ariadne import MutationType
from db import get_db
from schemas.category import CategoryCreate
from services.category.crud import create_category, update_category, delete_category
from core.auth import get_current_user
from app.exceptions import CustomAPIError

mutation = MutationType()


@mutation.field("createCategory")
async def resolve_create_category(_, info, name, description=None):
    try:
        db = get_db()
        user_id = get_current_user(info, db)
        category_data = CategoryCreate(name=name, description=description)
        result = await create_category(user_id, category_data)
        if result is None:
            raise ValueError("Category creation result cannot be null")
        return result
    except CustomAPIError as e:
        raise
    except Exception as e:
        raise Exception(f"Unexpected error in creating category: {str(e)}")


@mutation.field("updateCategory")
async def resolve_update_category(_, info, categoryId, name=None, description=None):
    try:
        user_id = get_current_user(info, get_db())
        update_data = {"name": name, "description": description}
        result = update_category(user_id, categoryId, update_data)
        return result
    except CustomAPIError as e:
        raise
    except Exception as e:
        raise Exception(f"Unexpected error in updating category: {str(e)}")


@mutation.field("deleteCategory")
async def resolve_delete_category(_, info, categoryId):
    try:
        user_id = get_current_user(info, get_db())
        result = delete_category(user_id, categoryId)
        return result
    except CustomAPIError as e:
        raise
    except Exception as e:
        raise Exception(f"Unexpected error in deleting category: {str(e)}")