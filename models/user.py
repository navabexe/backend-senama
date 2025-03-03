from pydantic.v1 import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: str
    password: Optional[str] = None
    roles: List[str] = Field(default_factory=list)  # ["admin", "vendor", "customer"]
    status: Optional[str] = "pending"  # (pending/active/blocked)
    otp: Optional[str] = None
    otp_expires_at: Optional[str] = None
    bio: Optional[str] = None
    avatar_urls: List[str] = Field(default_factory=list)
    phones: List[str] = Field(default_factory=list)
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    languages: List[str] = Field(default_factory=list)
    created_at: str
    updated_at: str