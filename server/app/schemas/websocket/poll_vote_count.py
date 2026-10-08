from pydantic import BaseModel , UUID4


class PollVoteCountWebSocketMessage(BaseModel):
    type: str
    poll_id: UUID4
    option_id: UUID4
    vote_count: int