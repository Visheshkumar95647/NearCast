from uuid import UUID

from pydantic import BaseModel


class PollResponse(BaseModel):
    id: UUID
    chat_id: UUID
    creator_id: UUID
    question: str
    is_multiple_choice: bool
    is_closed: bool

    model_config = {
        "from_attributes": True
    }


class PollVoteResponse(BaseModel):
    id: UUID
    poll_id: UUID
    option_id: UUID
    user_id: UUID

    model_config = {
        "from_attributes": True
    }