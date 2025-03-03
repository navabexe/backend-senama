from pydantic.v1 import BaseModel, Field
from typing import Optional

class Session(BaseModel):
    id: Optional[str] = None
    user_id: str
    token: str
    expires_at: str
    created_at: str