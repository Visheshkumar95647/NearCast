from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User
from app.schemas.activity.location import (
    ActivityLocationResponse,
    ActivityLocationUpdateRequest,
)
from app.services.activity.activity_location_service import (
    ActivityLocationService,
)


router = APIRouter(
    prefix="/activities",
    tags=["Activity Location"],
)

activity_location_service = ActivityLocationService()


@router.get(
    "/{activity_id}/location",
    response_model=ActivityLocationResponse,
)
def get_activity_location(
    activity_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    location, latitude, longitude = (
        activity_location_service.get_location_details(
            db=db,
            activity_id=activity_id,
        )
    )

    return ActivityLocationResponse(
        latitude=latitude,
        longitude=longitude,
        name=location.name,
    )


@router.patch(
    "/{activity_id}/location",
    response_model=ActivityLocationResponse,
)
def update_activity_location(
    activity_id: str,
    data: ActivityLocationUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    location = activity_location_service.create_or_update_location(
        db=db,
        activity_id=activity_id,
        latitude=data.latitude,
        longitude=data.longitude,
        name=data.name,
    )

    return ActivityLocationResponse(
        latitude=data.latitude,
        longitude=data.longitude,
        name=location.name,
    )


@router.delete(
    "/{activity_id}/location",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_activity_location(
    activity_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activity_location_service.delete_location(
        db=db,
        activity_id=activity_id,
    )