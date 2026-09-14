from datetime import datetime

from pydantic import BaseModel


class ActivityParticipantResponse(BaseModel):
    id: str
    user_id: str
    activity_id: str
    username: str
    status: str
    joined_at: datetime