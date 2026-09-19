from datetime import datetime

from pydantic import BaseModel


class SavedActivityResponse(BaseModel):
    id: str
    user_id: str
    activity_id: str
    created_at: datetime