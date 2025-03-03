from typing import List, Optional
from pydantic.v1 import BaseModel


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


class ProductCreate(BaseModel):
    vendor_id: str
    name: str
    category_ids: List[str]


class ProductResponse(BaseModel):
    id: str
    vendor_id: str
    names: List[str]
    short_descriptions: List[str]
    prices: List[Price]
    colors: List[Color]
    images: List[Image]
    video_urls: List[str]
    audio_files: List[AudioFile]
    technical_specs: List[Spec]
    tags: List[str]
    thumbnail_urls: List[str]
    suggested_products: List[str]
    status: str
    qr_code_url: Optional[str]
    category_ids: List[str]
    subcategory_ids: List[str]
    created_by: str
    created_at: str
    updated_by: str
    updated_at: str