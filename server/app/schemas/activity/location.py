from pydantic import BaseModel, Field


class ActivityLocationUpdateRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    name: str | None = Field(default=None, max_length=150)


class ActivityLocationResponse(BaseModel):
    latitude: float
    longitude: float
    name: str | None