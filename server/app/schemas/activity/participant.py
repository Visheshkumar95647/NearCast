from datetime import datetime

from pydantic import BaseModel ,UUID4


class ActivityParticipantResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    activity_id: str
    username: str
    status: str
    joined_at: datetime