from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from bson import ObjectId
import random
import string

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# تنظیمات رمزنگاری
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def json_serialize(data):
    return json.dumps(data, default=str)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_current_user(info, db):
    print("Entering get_current_user")  # دیباگ
    token = info.context.get("request").headers.get("Authorization")
    print(f"Token from headers: {token}")  # دیباگ
    if not token or not token.startswith("Bearer "):
        raise ValueError("No valid token provided")
    token = token.split("Bearer ")[1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Token payload: {payload}")  # دیباگ
    if not payload or "sub" not in payload:
        raise ValueError("Invalid token")

    session = db.sessions.find_one({"token": token, "user_id": payload["sub"]})
    print(f"Session: {session}")  # دیباگ
    if not session or datetime.fromisoformat(session["expires_at"]) < datetime.utcnow():
        raise ValueError("Session expired or invalid")

    return payload["sub"]


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def generate_otp(length=6):
    return ''.join(random.choice(string.digits) for _ in range(length))