from pydantic.v1 import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    phone: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    roles: List[str] = Field(default_factory=lambda: ["vendor"])
    bio: Optional[str] = None
    avatar_urls: Optional[List[str]] = Field(default_factory=list)
    phones: Optional[List[str]] = Field(default_factory=list)
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    languages: Optional[List[str]] = Field(default_factory=list)

class UserResponse(BaseModel):
    id: str
    phone: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    roles: List[str]
    status: str
    bio: Optional[str] = None
    avatar_urls: Optional[List[str]] = Field(default_factory=list)  # تغییر به Optional
    phones: Optional[List[str]] = Field(default_factory=list)      # تغییر به Optional
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    languages: Optional[List[str]] = Field(default_factory=list)   # تغییر به Optional
    created_at: str
    updated_at: str