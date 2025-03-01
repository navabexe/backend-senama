from pydantic.v1 import BaseModel, Field
from typing import Optional

class FollowBlock(BaseModel):
    id: Optional[str] = None
    follower_id: str
    following_id: str
    action: str
    created_at: str