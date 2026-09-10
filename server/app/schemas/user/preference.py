from pydantic import BaseModel, Field


class PreferenceUpdateRequest(BaseModel):
    max_distance_km: float | None = Field(
        default=None,
        gt=0,
    )
    preferred_group_size: int | None = Field(
        default=None,
        gt=0,
    )
    preferred_activity_type: str | None = Field(
        default=None,
        max_length=50,
    )
    notifications_enabled: bool | None = None


class PreferenceResponse(BaseModel):
    id: str
    max_distance_km: float
    preferred_group_size: int | None
    preferred_activity_type: str | None
    notifications_enabled: bool