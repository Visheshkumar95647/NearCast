from datetime import datetime

from pydantic import BaseModel, Field, UUID4


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
    id: UUID4

    group_id: UUID4

    sender_id: UUID4

    content: str

    sent_at: datetime

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }