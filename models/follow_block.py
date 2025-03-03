from typing import Optional
from pydantic.v1 import BaseModel


class FollowBlock(BaseModel):
    id: Optional[str] = None
    follower_id: str
    following_id: str
    action: str
    created_at: str