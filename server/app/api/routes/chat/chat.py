from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.chat.chat import ChatResponse
from app.models.user.user import User
from app.services.chat.chat_service import ChatService


router = APIRouter(
    prefix="/groups",
    tags=["Chat"],
)


chat_service = ChatService()


@router.get(
    "/{group_id}/chat",
    response_model=ChatResponse,
)
def get_or_create_group_chat(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return chat_service.get_or_create_group_chat(
        db=db,
        user_id=str(current_user.id),
        group_id=group_id,
    )


@router.get(
    "/chat/{chat_id}",
    response_model=ChatResponse,
)
def get_chat(
    chat_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return chat_service.get_chat_by_id(
        db=db,
        chat_id=chat_id,
        user_id=str(current_user.id),
    )