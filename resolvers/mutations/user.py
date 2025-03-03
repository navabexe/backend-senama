from ariadne import MutationType
from core.auth import get_current_user
from db import get_db
from schemas.user import UserCreate
from services.user.auth import create_user, request_otp, verify_otp, refresh_user_token, logout_user

mutation = MutationType()


@mutation.field("createUser")
async def resolve_create_user(_, info, phone, firstName=None, lastName=None, password=None, roles=["vendor"], bio=None,
                              avatarUrls=None, phones=None, birthdate=None, gender=None, languages=None):
    user_data = UserCreate(
        phone=phone,
        first_name=firstName,
        last_name=lastName,
        password=password,
        roles=roles,
        bio=bio,
        avatar_urls=avatarUrls,
        phones=phones,
        birthdate=birthdate,
        gender=gender,
        languages=languages
    )
    return create_user(user_data)


@mutation.field("requestOtp")
async def resolve_request_otp(_, info, phone):
    return request_otp(phone)


@mutation.field("verifyOtp")
async def resolve_verify_otp(_, info, phone, otp):
    return verify_otp(phone, otp)


@mutation.field("refreshToken")
async def resolve_refresh_token(_, info, refreshToken):
    return refresh_user_token(refreshToken)


@mutation.field("logoutUser")
async def resolve_logout_user(_, info):
    user_id = get_current_user(info, get_db())
    token = info.context.get("request").headers.get("Authorization").split("Bearer ")[1]
    return logout_user(user_id, token)