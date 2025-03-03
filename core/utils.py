import json
import random
import string
from passlib.context import CryptContext
from app.exceptions import validation_error

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def json_serialize(data):
    return json.dumps(data, default=str)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_otp(length=6):
    if length < 6:
        raise validation_error("OTP length", "must be at least 6 characters")
    return ''.join(random.choice(string.digits) for _ in range(length))