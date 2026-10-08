from uuid import UUID

from pydantic import BaseModel ,UUID4


class ChatResponse(BaseModel):
    id: UUID4
    group_id: UUID4
    name: str | None

    model_config = {
        "from_attributes": True
    }