from datetime import datetime

from pydantic import BaseModel , UUID4


class ChatWebSocketMessage(BaseModel):
    type: str
    message_id: UUID4
    chat_id: UUID4
    sender_id: UUID4
    content: str
    sent_at: datetime