from core.auth import get_current_user
from db import get_db
from services.user.profile import get_user_profile


async def resolve_user_profile(_, info):
    db = get_db()
    user_id = get_current_user(info, db)
    return get_user_profile(user_id)