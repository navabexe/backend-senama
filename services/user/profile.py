from bson import ObjectId
from app.exceptions import validation_error, not_found_error, server_error, CustomAPIError
from db import get_db
from schemas.user import UserResponse


def get_user_profile(user_id: str) -> UserResponse:
    db = get_db()
    try:
        try:
            user_id_obj = ObjectId(user_id)
        except ValueError:
            raise validation_error("User ID", "Invalid format")
        user = db.users.find_one({"_id": user_id_obj})
        if not user:
            raise not_found_error("User", user_id)
        user["id"] = str(user["_id"])
        del user["_id"]
        return UserResponse(**user)
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in retrieving profile: {str(e)}")
        raise