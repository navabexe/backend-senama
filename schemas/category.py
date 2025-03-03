from typing import Optional
from pydantic.v1 import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_by: str
    created_at: str
    updated_by: Optional[str]
    updated_at: str