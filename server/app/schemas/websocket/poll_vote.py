from datetime import datetime

from pydantic import BaseModel , UUID4


class PollVoteWebSocketMessage(BaseModel):
    type: str
    poll_id: UUID4
    option_id: UUID4
    user_id: UUID4
    voted_at: datetime