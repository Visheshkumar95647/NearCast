from datetime import datetime

from pydantic import BaseModel


class PollCloseWebSocketMessage(BaseModel):
    type: str
    poll_id: str
    chat_id: str
    closed_by: str
    closed_at: datetime