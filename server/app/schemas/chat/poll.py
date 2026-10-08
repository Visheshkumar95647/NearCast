
from pydantic import BaseModel ,UUID4


class PollResponse(BaseModel):
    id: UUID4
    chat_id: UUID4
    creator_id: UUID4
    question: str
    is_multiple_choice: bool
    is_closed: bool

    model_config = {
        "from_attributes": True
    }


class PollVoteResponse(BaseModel):
    id: UUID4
    poll_id: UUID4
    option_id: UUID4
    user_id: UUID4

    model_config = {
        "from_attributes": True
    }