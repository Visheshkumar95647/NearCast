from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User
from app.schemas.activity.saved_activity import SavedActivityResponse
from app.services.activity.saved_activity_service import (
    SavedActivityService,
)


router = APIRouter(
    prefix="/activities",
    tags=["Saved Activities"],
)

saved_activity_service = SavedActivityService()


@router.post(
    "/{activity_id}/save",
    response_model=SavedActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
def save_activity(
    activity_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    saved_activity = saved_activity_service.save_activity(
        db=db,
        user_id=str(current_user.id),
        activity_id=activity_id,
    )

    return SavedActivityResponse(
        id=str(saved_activity.id),
        user_id=str(saved_activity.user_id),
        activity_id=str(saved_activity.activity_id),
        created_at=saved_activity.created_at,
    )


@router.delete(
    "/{activity_id}/save",
    status_code=status.HTTP_204_NO_CONTENT,
)
def unsave_activity(
    activity_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    saved_activity_service.unsave_activity(
        db=db,
        user_id=str(current_user.id),
        activity_id=activity_id,
    )