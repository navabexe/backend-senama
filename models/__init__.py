from typing import List, Optional, Dict
from pydantic.v1 import Field, BaseModel

class Vendor(BaseModel):
    id: Optional[str] = None
    username: str
    name: str
    owner_id: str
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
    account_types: List[str]
    social_links: List[Dict] = Field(default_factory=list)
    messenger_links: List[Dict] = Field(default_factory=list)
    created_by: str
    created_at: str
    updated_by: str
    updated_at: str

class Product(BaseModel):
    id: Optional[str] = None
    vendor_id: str
    names: List[str]
    short_descriptions: List[str] = Field(default_factory=list)
    prices: List[Dict] = Field(default_factory=list)
    colors: List[Dict] = Field(default_factory=list)
    images: List[Dict] = Field(default_factory=list)
    video_urls: List[str] = Field(default_factory=list)
    audio_files: List[Dict] = Field(default_factory=list)
    technical_specs: List[Dict] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    thumbnail_urls: List[str] = Field(default_factory=list)
    suggested_products: List[str] = Field(default_factory=list)
    status: str
    qr_code_url: str
    category_ids: List[str] = Field(default_factory=list)
    subcategory_ids: List[str] = Field(default_factory=list)
    created_by: str
    created_at: str
    updated_by: str
    updated_at: str

class Log(BaseModel):
    id: Optional[str] = None
    model_type: str
    model_id: str
    action: str
    changed_by: str
    changed_at: str
    previous_data: Optional[str] = None
    new_data: str

class UserInteraction(BaseModel):
    id: Optional[str] = None
    user_id: str
    target_type: str
    target_id: str
    action: str
    timestamp: str
    details: Optional[str] = None