from datetime import datetime

from pydantic import BaseModel , UUID4


class PollCloseWebSocketMessage(BaseModel):
    type: str
    poll_id: UUID4
    chat_id: UUID4
    closed_by: UUID4
    closed_at: datetime