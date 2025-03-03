from datetime import datetime, UTC
from typing import List, Optional
from pydantic.v1 import BaseModel, Field


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
    avatar_urls: Optional[List[str]] = Field(default_factory=list)
    phones: Optional[List[str]] = Field(default_factory=list)
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    languages: Optional[List[str]] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())