from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat.chat import Chat


class ChatRepository:

    def get_by_group_id(
        self,
        db: Session,
        group_id: str,
    ) -> Chat | None:

        result = db.execute(
            select(Chat).where(
                Chat.group_id == group_id,
            )
        )

        return result.scalar_one_or_none()

    def get_by_id(
        self,
        db: Session,
        chat_id: str,
    ) -> Chat | None:

        return db.get(Chat, chat_id)

    def create(
        self,
        db: Session,
        chat: Chat,
    ) -> Chat:

        db.add(chat)
        db.commit()
        db.refresh(chat)

        return chat