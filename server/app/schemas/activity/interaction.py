from datetime import datetime

from pydantic import BaseModel


class ActivityInteractionRequest(BaseModel):
    interaction_type: str


class ActivityInteractionResponse(BaseModel):
    id: str
    user_id: str
    activity_id: str
    interaction_type: str
    occurred_at: datetime