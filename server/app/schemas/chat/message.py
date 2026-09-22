from datetime import datetime

from pydantic import BaseModel


class MessageResponse(BaseModel):
    id: str
    chat_id: str
    sender_id: str
    content: str
    sent_at: datetime
    created_at: datetime
    updated_at: datetime


class MessageCursor(BaseModel):
    sent_at: datetime
    message_id: str


class MessageListResponse(BaseModel):
    messages: list[MessageResponse]
    has_more: bool
    next_cursor: MessageCursor | None = None