from pydantic.v1 import BaseModel, Field
from typing import List, Optional

class Story(BaseModel):
    id: Optional[str] = None
    vendor_id: str
    media_url: str
    description: Optional[str] = None
    link: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: str
    updated_at: str