from pydantic import BaseModel


class PollOptionVoteCount(BaseModel):
    option_id: str
    vote_count: int


class PollStateWebSocketMessage(BaseModel):
    type: str
    poll_id: str
    counts: list[PollOptionVoteCount]