from pydantic.v1 import BaseModel, Field
from typing import Optional

class UserInteraction(BaseModel):
    id: Optional[str] = None
    user_id: str
    target_type: str
    target_id: str
    action: str
    timestamp: str