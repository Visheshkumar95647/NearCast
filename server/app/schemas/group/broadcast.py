from datetime import datetime

from pydantic import BaseModel, Field


class BroadcastCreate(BaseModel):

    content: str = Field(
        min_length=1,
        max_length=1000,
    )

    radius_meters: float = Field(
        ge=100,
        le=50000,
    )


class BroadcastResponse(BaseModel):

    id: str

    group_id: str

    sender_id: str

    content: str

    sent_at: datetime

    created_at: datetime

    updated_at: datetime