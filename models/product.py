from typing import List, Optional
from datetime import datetime, UTC
from pydantic.v1 import BaseModel, Field


class Price(BaseModel):
    type: str
    amount: float
    currency: str


class Color(BaseModel):
    name: str
    hex: str


class Image(BaseModel):
    url: str
    related_colors: List[str]
    textures: List[str]


class AudioFile(BaseModel):
    url: str
    label: str


class Spec(BaseModel):
    key: str
    value: str


class Product(BaseModel):
    id: Optional[str] = None
    vendor_id: str
    names: List[str]
    short_descriptions: List[str] = Field(default_factory=list)
    prices: List[Price] = Field(default_factory=list)
    colors: List[Color] = Field(default_factory=list)
    images: List[Image] = Field(default_factory=list)
    video_urls: List[str] = Field(default_factory=list)
    audio_files: List[AudioFile] = Field(default_factory=list)
    technical_specs: List[Spec] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    thumbnail_urls: List[str] = Field(default_factory=list)
    suggested_products: List[str] = Field(default_factory=list)
    status: Optional[str] = "draft"
    qr_code_url: Optional[str] = None
    category_ids: List[str]
    subcategory_ids: List[str] = Field(default_factory=list)
    created_by: str
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_by: str
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())