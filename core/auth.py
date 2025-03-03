from datetime import datetime, UTC, timedelta
import jwt
from app.config import config
from app.exceptions import auth_error


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    print(f"Created Access Token with expiry: {expire} (Unix: {int(expire.timestamp())})")
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, config.REFRESH_SECRET_KEY, algorithm=config.ALGORITHM)
    print(f"Created Refresh Token with expiry: {expire} (Unix: {int(expire.timestamp())})")
    return encoded_jwt


def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, config.REFRESH_SECRET_KEY, algorithms=[config.ALGORITHM])
        print(f"Decoded Refresh Token payload: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        raise auth_error("Refresh token has expired")
    except jwt.InvalidTokenError:
        raise auth_error("Invalid refresh token")


def get_current_user(info, db) -> str:
    print("Entering get_current_user")
    token = info.context.get("request").headers.get("Authorization")
    print(f"Token from headers: {token}")
    if not token or not token.startswith("Bearer "):
        raise auth_error("No valid token provided")
    token = token.split("Bearer ")[1]

    # Check blacklist
    if db.blacklist_tokens.find_one({"token": token}):
        raise auth_error("Token has been revoked")

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        print(f"Token payload: {payload}")
        exp_time = datetime.fromtimestamp(payload["exp"], tz=UTC)
        current_time = datetime.now(UTC)
        print(f"Token expiry (UTC): {exp_time}, Current time (UTC): {current_time}")
        if exp_time < current_time:
            print(f"Token manually detected as expired: {exp_time} < {current_time}")
            raise auth_error("Token has expired")
    except jwt.ExpiredSignatureError:
        print("Token expired (JWT lib)")
        raise auth_error("Token has expired")
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {str(e)}")
        raise auth_error("Invalid token")

    if "sub" not in payload:
        raise auth_error("Invalid token: user ID not found")

    session = db.sessions.find_one({"token": token, "user_id": payload["sub"]})
    print(f"Session: {session}")
    session_expire = datetime.fromisoformat(session["expires_at"]).replace(tzinfo=UTC) if session else None
    print(f"Session expiry (UTC): {session_expire}, Current time (UTC): {current_time}")
    if not session or session_expire < current_time:
        print(f"Session expired or not found: {session}")
        raise auth_error("Session has expired or is invalid")

    return payload["sub"]