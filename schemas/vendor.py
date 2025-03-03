from datetime import datetime
from typing import List, Optional
from pydantic.v1 import BaseModel


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


class VendorCreate(BaseModel):
    username: str
    name: str
    owner_name: str
    owner_phone: str
    address: str
    location: Location
    city: str
    province: str
    business_category_ids: List[str]


class VendorResponse(BaseModel):
    id: str
    username: str
    name: str
    owner_name: str
    owner_phone: str
    address: str
    location: Location
    city: str
    province: str
    logo_urls: List[str]
    banner_urls: List[str]
    bios: List[str]
    about_us: List[str]
    branches: List[Branch]
    business_details: List[BusinessDetail]
    visibility: bool
    attached_vendors: List[str]
    blocked_vendors: List[str]
    account_types: List[str]
    status: str
    vendor_type: str
    social_links: List[SocialLink]
    messenger_links: List[MessengerLink]
    followers_count: int
    following_count: int
    business_category_ids: List[str]
    created_by: str
    created_at: datetime
    updated_by: Optional[str]
    updated_at: datetime