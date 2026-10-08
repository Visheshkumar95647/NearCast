from datetime import datetime

from pydantic import BaseModel , UUID4


class PollWebSocketMessage(BaseModel):
    type: str
    poll_id: UUID4
    chat_id: UUID4
    creator_id: UUID4
    question: str
    is_multiple_choice: bool
    is_closed: bool
    created_at: datetime