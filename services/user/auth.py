import re
from datetime import datetime, UTC, timedelta
from bson import ObjectId
from app.config import config
from app.exceptions import validation_error, not_found_error, server_error, CustomAPIError, auth_error
from core.auth import create_access_token, create_refresh_token, decode_refresh_token
from core.utils import generate_otp, get_password_hash
from db import get_db
from models import Session, User
from schemas.user import UserCreate


def create_user(user_data: UserCreate) -> dict:
    db = get_db()
    try:
        if not re.match(r"^\+?[0-9]{10,14}$", user_data.phone):
            raise validation_error("Phone number", "Format must be like +989123456789 or 09123456789")
        if db.users.find_one({"phone": user_data.phone}):
            raise validation_error("Phone number", f"{user_data.phone} is already registered")
        if user_data.password and len(user_data.password) < 6:
            raise validation_error("Password", "Must be at least 6 characters")

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
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat()
        )
        result = db.users.insert_one(user.dict())
        user_id = str(result.inserted_id)
        return {"id": user_id, "otp": otp}
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in creating user: {str(e)}")
        raise


def request_otp(phone: str) -> dict:
    db = get_db()
    try:
        user = db.users.find_one({"phone": phone})
        if not user:
            raise not_found_error("User", phone)

        otp = generate_otp()
        db.users.update_one(
            {"_id": ObjectId(user["_id"])},
            {"$set": {"otp": otp, "otp_expires_at": (datetime.now(UTC) + timedelta(minutes=5)).isoformat()}}
        )
        return {"id": str(user["_id"]), "otp": otp}
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in requesting OTP: {str(e)}")
        raise


def verify_otp(phone: str, otp: str) -> dict:
    db = get_db()
    try:
        user = db.users.find_one({"phone": phone})
        if not user:
            raise not_found_error("User", phone)

        if "otp" not in user or "otp_expires_at" not in user:
            raise validation_error("OTP code", "Not registered for this number")
        if not re.match(r"^\d{6}$", otp):
            raise validation_error("OTP code", "Must be 6 digits")

        expires_at = datetime.fromisoformat(user["otp_expires_at"])
        if user["otp"] != otp:
            raise validation_error("OTP code", "Incorrect")
        if expires_at < datetime.now(UTC):
            raise validation_error("OTP code", "Expired")

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
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": str(user["_id"])
        }
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in verifying OTP: {str(e)}")
        raise


def refresh_user_token(refresh_token: str) -> dict:
    db = get_db()
    try:
        payload = decode_refresh_token(refresh_token)
        user_id = payload["sub"]
        session = db.sessions.find_one({"user_id": user_id})
        if not session:
            raise not_found_error("Session", user_id)

        if db.blacklist_tokens.find_one({"token": refresh_token}):
            raise auth_error("Refresh token has been revoked")

        access_token = create_access_token(data={"sub": user_id})
        session_expiry = datetime.now(UTC) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        db.sessions.update_one(
            {"user_id": user_id},
            {"$set": {"token": access_token, "expires_at": session_expiry.isoformat()}}
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user_id
        }
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in refreshing token: {str(e)}")
        raise


def logout_user(user_id: str, token: str) -> dict:
    db = get_db()
    try:
        try:
            ObjectId(user_id)
        except ValueError:
            raise validation_error("User ID", "Invalid format")
        db.sessions.delete_one({"user_id": user_id, "token": token})
        db.blacklist_tokens.insert_one({
            "token": token,
            "user_id": user_id,
            "blacklisted_at": datetime.now(UTC).isoformat(),
            "expires_at": (datetime.now(UTC) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)).isoformat()
        })
        return {"message": "Successfully logged out"}
    except Exception as e:
        if not isinstance(e, CustomAPIError):
            raise server_error(f"Unexpected error in logout: {str(e)}")
        raise