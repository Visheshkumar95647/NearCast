from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.models.chat.message import Message


class MessageRepository:
    def create(
        self,
        db: Session,
        message: Message,
    ) -> Message:
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def get_by_id(
        self,
        db: Session,
        message_id: str,
    ) -> Message | None:
        return db.get(Message, message_id)

    def get_by_chat_id(
        self,
        db: Session,
        chat_id: str,
        limit: int = 50,
        before_sent_at: datetime | None = None,
        before_message_id: UUID | None = None,
    ) -> tuple[list[Message], bool]:
        query = select(Message).where(
            Message.chat_id == chat_id,
        )

        if before_sent_at is not None and before_message_id is not None:
            query = query.where(
                # if message datetime is less then give or if message datetime is same than give message whose id is less then before id
                or_(
                    Message.sent_at < before_sent_at,
                    and_(
                        Message.sent_at == before_sent_at,
                        Message.id < before_message_id,
                    ),
                )
            )

        query = (
            query
            .order_by(
                Message.sent_at.desc(),
                Message.id.desc(),
            )
            .limit(limit + 1)
        )

        result = db.execute(query)

        messages = list(result.scalars().all())

        has_more = len(messages) > limit

        messages = messages[:limit]

        messages.reverse()

        return messages, has_more