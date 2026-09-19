from datetime import datetime

from pydantic import BaseModel


class BroadcastWebSocketMessage(BaseModel):

    type: str

    broadcast_id: str

    group_id: str

    sender_id: str

    content: str

    sent_at: datetime