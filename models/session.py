from typing import Optional
from pydantic.v1 import BaseModel


class Session(BaseModel):
    id: Optional[str] = None
    user_id: str
    token: str
    expires_at: str
    created_at: str