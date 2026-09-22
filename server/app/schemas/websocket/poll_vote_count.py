from pydantic import BaseModel


class PollVoteCountWebSocketMessage(BaseModel):
    type: str
    poll_id: str
    option_id: str
    vote_count: int