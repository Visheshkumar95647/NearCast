from pydantic import BaseModel, Field , UUID4


class AddInterestRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class InterestResponse(BaseModel):
    id: UUID4
    name: str