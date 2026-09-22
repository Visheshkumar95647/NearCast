from fastapi import WebSocket
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user.user import User
from app.repositories.chat.chat_repository import ChatRepository
from app.repositories.group.group_member_repository import GroupMemberRepository
from app.services.auth.auth_service import AuthService


auth_service = AuthService()
chat_repository = ChatRepository()
group_member_repository = GroupMemberRepository()


async def get_current_chat_websocket_user(
    websocket: WebSocket,
    chat_id: str,
) -> User:
    token = websocket.cookies.get("access_token")

    if not token:
        await websocket.close(code=1008)
        raise RuntimeError("Authentication required")

    db: Session = SessionLocal()

    try:
        current_user = auth_service.get_current_user(
            db=db,
            token=token,
        )

        chat = chat_repository.get_by_id(
            db=db,
            chat_id=chat_id,
        )

        if not chat:
            await websocket.close(code=1008)
            raise RuntimeError("Chat not found")

        group_member = group_member_repository.get_by_user_and_group(
            db=db,
            user_id=str(current_user.id),
            group_id=str(chat.group_id),
        )

        if not group_member:
            await websocket.close(code=1008)
            raise RuntimeError("You are not a member of this group")

        return current_user

    finally:
        db.close()