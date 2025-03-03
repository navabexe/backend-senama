from datetime import datetime, UTC
from typing import List, Optional
from pydantic.v1 import BaseModel, Field


class Location(BaseModel):
    lat: float
    lng: float


class Branch(BaseModel):
    label: str
    city: str
    province: str
    address: str
    location: Location
    phones: List[str]
    emails: List[str]


class BusinessDetail(BaseModel):
    type: str
    values: List[str]


class SocialLink(BaseModel):
    platform: str
    url: str


class MessengerLink(BaseModel):
    platform: str
    url: str


class Vendor(BaseModel):
    id: Optional[str] = None
    username: str
    name: str
    owner_name: str
    owner_phone: str
    address: str
    location: Location
    city: str
    province: str
    logo_urls: List[str] = Field(default_factory=list)
    banner_urls: List[str] = Field(default_factory=list)
    bios: List[str] = Field(default_factory=list)
    about_us: List[str] = Field(default_factory=list)
    branches: List[Branch] = Field(default_factory=list)
    business_details: List[BusinessDetail] = Field(default_factory=list)
    visibility: bool = True
    attached_vendors: List[str] = Field(default_factory=list)
    blocked_vendors: List[str] = Field(default_factory=list)
    account_types: List[str] = Field(default_factory=lambda: ["free"])
    status: Optional[str] = "pending"
    vendor_type: Optional[str] = "basic"
    social_links: List[SocialLink] = Field(default_factory=list)
    messenger_links: List[MessengerLink] = Field(default_factory=list)
    followers_count: int = 0
    following_count: int = 0
    business_category_ids: List[str]
    created_by: str
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_by: Optional[str] = None
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())