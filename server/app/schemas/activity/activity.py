from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ActivityCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str | None = None
    group_id: UUID | None = None
    starts_at: datetime
    ends_at: datetime | None = None
    is_public: bool = True


class ActivityUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    group_id: UUID | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    is_public: bool | None = None
    is_active: bool | None = None


class ActivityResponse(BaseModel):
    id: UUID
    group_id: UUID | None
    title: str
    description: str | None
    starts_at: datetime
    ends_at: datetime | None
    is_public: bool
    is_active: bool

    model_config = {
        "from_attributes": True
    }