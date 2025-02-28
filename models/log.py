from pydantic.v1 import BaseModel
from typing import Optional

class Log(BaseModel):
    id: Optional[str] = None
    model_type: str
    model_id: str
    action: str
    changed_by: str
    changed_at: str
    previous_data: Optional[str] = None
    new_data: str