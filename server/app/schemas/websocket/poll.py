from datetime import datetime

from pydantic import BaseModel


class PollWebSocketMessage(BaseModel):
    type: str
    poll_id: str
    chat_id: str
    creator_id: str
    question: str
    is_multiple_choice: bool
    is_closed: bool
    created_at: datetime