from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.chat.message import Message
from app.schemas.chat.message import MessageListResponse
from app.repositories.chat.chat_repository import ChatRepository
from app.repositories.chat.message_repository import MessageRepository
from app.repositories.group.group_member_repository import GroupMemberRepository
from app.schemas.websocket.chat import ChatWebSocketMessage
from server.app.services.recommendation.websocket.manager import manager
from uuid import UUID

class MessageService:
    def __init__(self):
        self.message_repository = MessageRepository()
        self.chat_repository = ChatRepository()
        self.group_member_repository = GroupMemberRepository()

    async def send_message(
        self,
        db: Session,
        user_id: str,
        chat_id: str,
        content: str,
    ) -> Message:
        chat = self.chat_repository.get_by_id(
            db=db,
            chat_id=chat_id,
        )

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )

        group_member = self.group_member_repository.get_by_user_and_group(
            db=db,
            user_id=user_id,
            group_id=str(chat.group_id),
        )

        if not group_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this group",
            )

        message = Message(
            chat_id=chat_id,
            sender_id=user_id,
            content=content,
            sent_at=datetime.now(timezone.utc),
        )

        message = self.message_repository.create(
            db=db,
            message=message,
        )

        member_user_ids = self.group_member_repository.get_user_ids_by_group_id(
            db=db,
            group_id=str(chat.group_id),
        )

        websocket_message = ChatWebSocketMessage(
            type="message",
            message_id=str(message.id),
            chat_id=str(message.chat_id),
            sender_id=str(message.sender_id),
            content=message.content,
            sent_at=message.sent_at,
        )

        await manager.send_to_users(
            user_ids=member_user_ids,
            message=websocket_message.model_dump(mode="json"),
        )

        return message

    def get_chat_messages(
    self,
    db: Session,
    user_id: str,
    chat_id: str,
    limit: int = 50,
    before_sent_at: datetime | None = None,
    before_message_id: UUID | None = None,
) -> MessageListResponse:
    chat = self.chat_repository.get_by_id(
        db=db,
        chat_id=chat_id,
    )

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )

    group_member = self.group_member_repository.get_by_user_and_group(
        db=db,
        user_id=user_id,
        group_id=str(chat.group_id),
    )

    if not group_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this group",
        )

    messages, has_more = self.message_repository.get_by_chat_id(
        db=db,
        chat_id=chat_id,
        limit=limit,
        before_sent_at=before_sent_at,
        before_message_id=before_message_id,
    )

    message_responses = [
        MessageResponse(
            id=str(message.id),
            chat_id=str(message.chat_id),
            sender_id=str(message.sender_id),
            content=message.content,
            sent_at=message.sent_at,
            created_at=message.created_at,
            updated_at=message.updated_at,
        )
        for message in messages
    ]

    next_cursor = None

    if has_more and messages:
        oldest_message = messages[0]

        next_cursor = MessageCursor(
            sent_at=oldest_message.sent_at,
            message_id=str(oldest_message.id),
        )

    return MessageListResponse(
        messages=message_responses,
        has_more=has_more,
        next_cursor=next_cursor,
    )