from datetime import datetime

from pydantic import BaseModel


class GroupMemberResponse(BaseModel):
    id: str
    user_id: str
    group_id: str
    username: str
    role: str
    joined_at: datetime


class JoinRequestResponse(BaseModel):
    id: str
    user_id: str
    group_id: str
    username: str
    status: str
    requested_at: datetime
    reviewed_at: datetime | None