from datetime import datetime

from pydantic import BaseModel, UUID4


class GroupMemberResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    group_id: UUID4
    username: str
    role: str
    joined_at: datetime


class JoinRequestResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    group_id: UUID4
    status: str
    requested_at: datetime
    reviewed_at: datetime | None