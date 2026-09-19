from datetime import datetime

from pydantic import BaseModel, Field


class GroupLocationCreateRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    name: str | None = Field(default=None, max_length=150)


class GroupLocationUpdateRequest(BaseModel):
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    name: str | None = Field(default=None, max_length=150)


class GroupLocationResponse(BaseModel):
    id: str
    group_id: str
    latitude: float
    longitude: float
    name: str | None
    created_at: datetime
    updated_at: datetime