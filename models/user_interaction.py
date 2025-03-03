from datetime import datetime, UTC
from typing import Optional
from pydantic.v1 import BaseModel, Field


class UserInteraction(BaseModel):
    id: Optional[str] = None
    user_id: str
    target_type: str
    target_id: str
    action: str
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    details: Optional[str] = None