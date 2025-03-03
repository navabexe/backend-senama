from datetime import datetime, UTC
from typing import Optional
from pydantic.v1 import BaseModel, Field


class Category(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    created_by: str
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_by: Optional[str] = None
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())