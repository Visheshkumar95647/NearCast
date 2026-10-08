from pydantic import BaseModel, UUID4


class PollOptionVoteCount(BaseModel):
    option_id: UUID4
    vote_count: int


class PollStateWebSocketMessage(BaseModel):
    type: str
    poll_id: UUID4
    counts: list[PollOptionVoteCount]