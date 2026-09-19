from pydantic import BaseModel, Field


class GroupCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    is_private: bool = False


class GroupUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    is_private: bool | None = None
    is_active: bool | None = None


class GroupResponse(BaseModel):
    id: str
    name: str
    description: str | None
    is_private: bool
    is_active: bool