from pydantic import BaseModel, Field


class AddInterestRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class InterestResponse(BaseModel):
    id: str
    name: str