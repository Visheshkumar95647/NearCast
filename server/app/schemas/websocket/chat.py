from datetime import datetime

from pydantic import BaseModel


class ChatWebSocketMessage(BaseModel):
    type: str
    message_id: str
    chat_id: str
    sender_id: str
    content: str
    sent_at: datetime