from datetime import datetime, UTC
from typing import Optional
from pydantic.v1 import BaseModel, Field


class Log(BaseModel):
    id: Optional[str] = None
    model_type: str
    model_id: str
    action: str
    changed_by: str
    changed_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    previous_data: Optional[str] = None
    new_data: str