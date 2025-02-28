from pydantic.v1 import BaseModel, Field
from typing import List, Optional, Dict

class Vendor(BaseModel):
    id: Optional[str] = None
    username: str
    name: str
    owner_name: str
    owner_phone: str
    address: str
    location: Dict[str, float]
    city: str
    province: str
    category_ids: List[str]  # اضافه کردن دسته‌بندی اجباری
    logo_urls: List[str] = Field(default_factory=list)
    banner_urls: List[str] = Field(default_factory=list)
    bios: List[str] = Field(default_factory=list)
    about_us: List[str] = Field(default_factory=list)
    followers_count: int = 0
    following_count: int = 0
    branches: List[Dict] = Field(default_factory=list)
    business_details: List[Dict] = Field(default_factory=list)
    visibility: bool = True
    attached_vendors: List[str] = Field(default_factory=list)
    blocked_vendors: List[str] = Field(default_factory=list)
    account_types: List[str] = Field(default_factory=list)
    social_links: List[Dict] = Field(default_factory=list)
    messenger_links: List[Dict] = Field(default_factory=list)
    created_by: str
    created_at: str
    updated_by: str
    updated_at: str