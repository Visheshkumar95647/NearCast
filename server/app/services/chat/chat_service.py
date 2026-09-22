from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.chat.chat import Chat
from app.repositories.chat.chat_repository import ChatRepository
from app.repositories.group.group_member_repository import GroupMemberRepository


class ChatService:

    def __init__(self):
        self.chat_repository = ChatRepository()
        self.group_member_repository = GroupMemberRepository()

    def get_or_create_group_chat(
        self,
        db: Session,
        user_id: str,
        group_id: str,
    ) -> Chat:

        group_member = self.group_member_repository.get_by_user_and_group(
            db=db,
            user_id=user_id,
            group_id=group_id,
        )

        if not group_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this group",
            )

        chat = self.chat_repository.get_by_group_id(
            db=db,
            group_id=group_id,
        )

        if chat:
            return chat

        chat = Chat(
            group_id=group_id,
            name=None,
        )

        return self.chat_repository.create(
            db=db,
            chat=chat,
        )

    def get_chat_by_id(
    self,
    db: Session,
    chat_id: str,
    user_id: str,
) -> Chat:

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

    return chat