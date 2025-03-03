from pydantic.v1 import BaseModel, Field
from typing import List, Optional
from datetime import datetime, UTC

class User(BaseModel):
    id: Optional[str] = None
    phone: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    roles: List[str] = Field(default_factory=lambda: ["vendor"])
    status: Optional[str] = "pending"
    otp: Optional[str] = None
    otp_expires_at: Optional[str] = None
    bio: Optional[str] = None
    avatar_urls: Optional[List[str]] = Field(default_factory=list)  # تغییر به Optional
    phones: Optional[List[str]] = Field(default_factory=list)      # تغییر به Optional
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    languages: Optional[List[str]] = Field(default_factory=list)   # تغییر به Optional
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())  # تغییر به str
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())  # تغییر به str