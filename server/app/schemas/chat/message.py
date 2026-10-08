from datetime import datetime

from pydantic import BaseModel ,UUID4


class MessageResponse(BaseModel):
    id: UUID4
    chat_id: UUID4
    sender_id: UUID4
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