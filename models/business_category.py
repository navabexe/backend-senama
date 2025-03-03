from typing import Optional
from pydantic.v1 import BaseModel


class BusinessCategory(BaseModel):
    id: Optional[str] = None
    name: str
    created_at: str
    updated_at: str