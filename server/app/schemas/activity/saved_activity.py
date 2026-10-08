from datetime import datetime

from pydantic import BaseModel ,UUID4


class SavedActivityResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    activity_id: UUID4
    created_at: datetime