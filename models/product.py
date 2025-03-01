from pydantic.v1 import BaseModel, Field
from typing import List, Optional, Dict

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
    category_ids: List[str]
    subcategory_ids: List[str] = Field(default_factory=list)
    created_by: str
    created_at: str
    updated_by: str
    updated_at: str