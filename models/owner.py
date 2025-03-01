from pydantic.v1 import BaseModel, Field
from typing import List, Optional

class Owner(BaseModel):
    id: Optional[str] = None
    first_name: str
    last_name: str
    phone: str
    bio: Optional[str] = None
    avatar_urls: List[str] = Field(default_factory=list)
    phones: List[str] = Field(default_factory=list)
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    languages: List[str] = Field(default_factory=list)
    created_at: str
    updated_at: str