from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.chat.message import Message
from app.models.user.user import User
from app.schemas.chat.message import MessageListResponse
from app.services.chat.message_service import MessageService


router = APIRouter(
    prefix="/chat",
    tags=["Chat Messages"],
)

message_service = MessageService()


class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)


@router.post(
    "/{chat_id}/messages",
    response_model=Message,
)
async def send_message(
    chat_id: str,
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await message_service.send_message(
        db=db,
        user_id=str(current_user.id),
        chat_id=chat_id,
        content=data.content,
    )


@router.get(
    "/{chat_id}/messages",
    response_model=MessageListResponse,
)
def get_chat_messages(
    chat_id: str,
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    before_sent_at: datetime | None = Query(
        default=None,
    ),
    before_message_id: UUID | None = Query(
        default=None,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if (before_sent_at is None) != (before_message_id is None):
        raise HTTPException(
            status_code=400,
            detail="before_sent_at and before_message_id must be provided together",
        )

    return message_service.get_chat_messages(
        db=db,
        user_id=str(current_user.id),
        chat_id=chat_id,
        limit=limit,
        before_sent_at=before_sent_at,
        before_message_id=before_message_id,
    )