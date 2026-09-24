from uuid import UUID

from pydantic import BaseModel


class ChatResponse(BaseModel):
    id: UUID
    group_id: UUID
    name: str | None

    model_config = {
        "from_attributes": True
    }