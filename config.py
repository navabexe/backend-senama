import os
from dotenv import load_dotenv

load_dotenv()  # بارگذاری متغیرها از .env

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/senama_db")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "your-refresh-secret-key")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

config = Config()