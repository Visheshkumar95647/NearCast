from datetime import datetime

from pydantic import BaseModel , UUID4


class ActivityInteractionRequest(BaseModel):
    interaction_type: str


class ActivityInteractionResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    activity_id: UUID4
    interaction_type: str
    occurred_at: datetime