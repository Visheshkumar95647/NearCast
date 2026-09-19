from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User
from app.schemas.activity.activity import (
    ActivityCreateRequest,
    ActivityResponse,
    ActivityUpdateRequest,
)
from app.services.activity.activity_service import ActivityService


router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
)

activity_service = ActivityService()


@router.post(
    "",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_activity(
    data: ActivityCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return activity_service.create_activity(
        db=db,
        title=data.title,
        description=data.description,
        group_id=data.group_id,
        starts_at=data.starts_at,
        ends_at=data.ends_at,
        is_public=data.is_public,
    )


@router.get(
    "/{activity_id}",
    response_model=ActivityResponse,
)
def get_activity(
    activity_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return activity_service.get_activity(
        db=db,
        activity_id=activity_id,
    )


@router.patch(
    "/{activity_id}",
    response_model=ActivityResponse,
)
def update_activity(
    activity_id: str,
    data: ActivityUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return activity_service.update_activity(
        db=db,
        activity_id=activity_id,
        title=data.title,
        description=data.description,
        group_id=data.group_id,
        starts_at=data.starts_at,
        ends_at=data.ends_at,
        is_public=data.is_public,
        is_active=data.is_active,
    )


@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_activity(
    activity_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activity_service.delete_activity(
        db=db,
        activity_id=activity_id,
    )