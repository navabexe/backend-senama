from pydantic.v1 import BaseModel, Field
from typing import Optional

class Category(BaseModel):
    id: Optional[str] = None
    name: str
    created_at: str
    updated_at: str

class Subcategory(BaseModel):
    id: Optional[str] = None
    category_id: str
    name: str
    created_at: str
    updated_at: str