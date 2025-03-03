from datetime import datetime, UTC
from typing import List, Optional
from pydantic.v1 import BaseModel, Field


class Story(BaseModel):
    id: Optional[str] = None
    vendor_id: str
    media_url: str
    description: Optional[str] = None
    link: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())