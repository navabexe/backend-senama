import re
from datetime import datetime, UTC, timedelta
from bson import ObjectId
from db import get_db
from models.user import User
from models.session import Session
from config import config
from utils import create_access_token, create_refresh_token, generate_otp, get_password_hash, decode_refresh_token
from schemas.user import UserCreate, UserResponse


def create_user(user_data: UserCreate) -> dict:
    db = get_db()
    if not re.match(r"^\+?[0-9]{10,14}$", user_data.phone):
        raise ValueError("Phone number format invalid (e.g., +989123456789 or 09123456789)")
    if db.users.find_one({"phone": user_data.phone}):
        raise ValueError(f"Phone {user_data.phone} already exists")
    if user_data.password and len(user_data.password) < 6:
        raise ValueError("Password must be at least 6 characters long")

    otp = generate_otp()
    hashed_password = get_password_hash(user_data.password) if user_data.password else None
    user = User(
        phone=user_data.phone,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password=hashed_password,
        roles=user_data.roles,
        status="pending",
        otp=otp,
        otp_expires_at=(datetime.now(UTC) + timedelta(minutes=5)).isoformat(),
        bio=user_data.bio,
        avatar_urls=user_data.avatar_urls,
        phones=user_data.phones,
        birthdate=user_data.birthdate,
        gender=user_data.gender,
        languages=user_data.languages,
        created_at=datetime.now(UTC).isoformat(),  # به صورت str
        updated_at=datetime.now(UTC).isoformat()  # به صورت str
    )
    result = db.users.insert_one(user.dict())
    user_id = str(result.inserted_id)
    return {"id": user_id, "otp": otp}


def request_otp(phone: str) -> dict:
    db = get_db()
    user = db.users.find_one({"phone": phone})
    if not user:
        raise ValueError(f"Phone {phone} not found")

    otp = generate_otp()
    db.users.update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": {"otp": otp, "otp_expires_at": (datetime.now(UTC) + timedelta(minutes=5)).isoformat()}}
    )
    print(f"Generated OTP for {phone}: {otp}")
    return {"id": str(user["_id"]), "otp": otp}


def verify_otp(phone: str, otp: str) -> dict:
    db = get_db()
    user = db.users.find_one({"phone": phone})
    if not user:
        raise ValueError("Phone not found")

    if "otp" not in user or "otp_expires_at" not in user:
        raise ValueError("No OTP found for this phone")
    if not re.match(r"^\d{6}$", otp):
        raise ValueError("OTP must be a 6-digit number")

    expires_at = datetime.fromisoformat(user["otp_expires_at"])
    if user["otp"] != otp:
        raise ValueError("Invalid OTP")
    if expires_at < datetime.now(UTC):
        raise ValueError("OTP has expired")

    db.users.update_one({"_id": ObjectId(user["_id"])}, {"$unset": {"otp": "", "otp_expires_at": ""}})
    access_token = create_access_token(data={"sub": str(user["_id"])})
    refresh_token = create_refresh_token(data={"sub": str(user["_id"])})
    session_expiry = datetime.now(UTC) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    session = Session(
        user_id=str(user["_id"]),
        token=access_token,
        expires_at=session_expiry.isoformat(),
        created_at=datetime.now(UTC).isoformat()
    )
    result = db.sessions.insert_one(session.dict())
    session.id = str(result.inserted_id)
    print(
        f"Created session with ID: {session.id}, Access Token: {access_token}, Refresh Token: {refresh_token}, Session Expiry: {session_expiry}")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": str(user["_id"])
    }


def get_user_profile(user_id: str) -> UserResponse:
    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise ValueError("User not found")
    user["id"] = str(user["_id"])
    del user["_id"]
    return UserResponse(**user)


def refresh_user_token(refresh_token: str) -> dict:
    db = get_db()
    payload = decode_refresh_token(refresh_token)
    user_id = payload["sub"]
    session = db.sessions.find_one({"user_id": user_id})
    if not session:
        raise ValueError("No active session found")

    access_token = create_access_token(data={"sub": user_id})
    session_expiry = datetime.now(UTC) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    db.sessions.update_one(
        {"user_id": user_id},
        {"$set": {"token": access_token, "expires_at": session_expiry.isoformat()}}
    )
    print(f"Refreshed access token for user {user_id}: {access_token}, New Session Expiry: {session_expiry}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id
    }


def logout_user(user_id: str, token: str) -> dict:
    db = get_db()
    db.sessions.delete_one({"user_id": user_id, "token": token})
    return {"message": "Logged out successfully"}