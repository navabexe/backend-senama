from pydantic.v1 import BaseModel
from typing import Optional

class UserInteraction(BaseModel):
    id: Optional[str] = None
    user_id: str
    target_type: str
    target_id: str
    action: str
    timestamp: str
    details: Optional[str] = None