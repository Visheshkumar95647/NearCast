from datetime import datetime

from pydantic import BaseModel


class PollVoteWebSocketMessage(BaseModel):
    type: str
    poll_id: str
    option_id: str
    user_id: str
    voted_at: datetime