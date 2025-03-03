from ariadne import MutationType
from db import get_db
from models.user import User
from models.session import Session
from datetime import datetime, UTC, timedelta
from bson import ObjectId
from utils import json_serialize, create_access_token, generate_otp, get_password_hash, get_current_user

mutation = MutationType()


@mutation.field("createUser")
async def resolve_create_user(_, info, phone, firstName=None, lastName=None, password=None, roles=["vendor"], bio=None,
                              avatarUrls=None, phones=None, birthdate=None, gender=None, languages=None):
    db = get_db()
    if db.users.find_one({"phone": phone}):
        raise ValueError(f"Phone {phone} already exists")

    otp = generate_otp()
    hashed_password = get_password_hash(password) if password else None
    user = User(
        phone=phone,
        first_name=firstName,
        last_name=lastName,
        password=hashed_password,
        roles=roles,
        status="pending",  # پیش‌فرض در انتظار تأیید
        otp=otp,
        otp_expires_at=(datetime.utcnow() + timedelta(minutes=5)).isoformat(),
        bio=bio,
        avatar_urls=avatarUrls or [],
        phones=phones or [],
        birthdate=birthdate,
        gender=gender,
        languages=languages or [],
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    result = db.users.insert_one(user.dict())
    user_id = str(result.inserted_id)
    user.id = user_id
    print(f"Created user with ID: {user_id}, OTP: {otp}")
    return {"id": user_id, "otp": otp}


@mutation.field("verifyOtp")
async def resolve_verify_otp(_, info, phone, otp):
    db = get_db()
    user = db.users.find_one({"phone": phone})
    if not user:
        raise ValueError("Phone not found")

    if "otp" not in user or "otp_expires_at" not in user:
        raise ValueError("No OTP found for this phone")

    expires_at = datetime.fromisoformat(user["otp_expires_at"])
    if user["otp"] != otp:
        raise ValueError("Invalid OTP")
    if expires_at < datetime.utcnow():
        raise ValueError("OTP has expired")

    db.users.update_one({"_id": ObjectId(user["_id"])}, {"$unset": {"otp": "", "otp_expires_at": ""}})
    access_token = create_access_token(data={"sub": str(user["_id"])})
    session = Session(
        user_id=str(user["_id"]),
        token=access_token,
        expires_at=(datetime.utcnow() + timedelta(minutes=30)).isoformat(),
        created_at=datetime.now(UTC).isoformat()
    )
    result = db.sessions.insert_one(session.dict())
    session.id = str(result.inserted_id)
    print(f"Created session with ID: {session.id}")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user["_id"])
    }


@mutation.field("logoutUser")
async def resolve_logout_user(_, info):
    db = get_db()
    user_id = get_current_user(info, db)
    token = info.context.get("request").headers.get("Authorization").split("Bearer ")[1]
    db.sessions.delete_one({"user_id": user_id, "token": token})
    return {"message": "Logged out successfully"}


@mutation.field("activateUser")
async def resolve_activate_user(_, info, userId):
    db = get_db()
    admin_id = get_current_user(info, db)
    admin = db.users.find_one({"_id": ObjectId(admin_id)})
    if "admin" not in admin["roles"]:
        raise ValueError("Only admins can activate users")

    user = db.users.find_one({"_id": ObjectId(userId)})
    if not user:
        raise ValueError(f"User with ID {userId} not found")

    db.users.update_one({"_id": ObjectId(userId)}, {"$set": {"status": "active"}})
    return {"message": f"User {userId} activated successfully"}


@mutation.field("regenerateOtp")
async def resolve_regenerate_otp(_, info, phone):
    db = get_db()
    user = db.users.find_one({"phone": phone})
    if not user:
        raise ValueError(f"Phone {phone} not found")

    otp = generate_otp()
    db.users.update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": {"otp": otp, "otp_expires_at": (datetime.utcnow() + timedelta(minutes=5)).isoformat()}}
    )
    print(f"Regenerated OTP for {phone}: {otp}")
    return {"id": str(user["_id"]), "otp": otp}