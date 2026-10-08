from datetime import datetime

from uuid import UUID

from pydantic import BaseModel


class BroadcastWebSocketMessage(BaseModel):

    type: str

    broadcast_id: str

    group_id: UUID

    sender_id: str

    content: str

    sent_at: datetime