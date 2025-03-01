from pydantic.v1 import BaseModel, Field
from typing import Optional

class BusinessCategory(BaseModel):
    id: Optional[str] = None
    name: str
    created_at: str
    updated_at: str