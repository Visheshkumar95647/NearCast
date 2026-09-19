from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User
from app.schemas.group.group_location import (
    GroupLocationCreateRequest,
    GroupLocationResponse,
    GroupLocationUpdateRequest,
)
from app.services.group.group_location_service import GroupLocationService


router = APIRouter(
    prefix="/groups",
    tags=["Group Locations"],
)

group_location_service = GroupLocationService()


@router.post(
    "/{group_id}/location",
    response_model=GroupLocationResponse,
)
def create_group_location(
    group_id: str,
    request: GroupLocationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return group_location_service.create_location(
        db=db,
        group_id=group_id,
        latitude=request.latitude,
        longitude=request.longitude,
        name=request.name,
    )


@router.get(
    "/{group_id}/location",
    response_model=GroupLocationResponse,
)
def get_group_location(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return group_location_service.get_location(
        db=db,
        group_id=group_id,
    )


@router.patch(
    "/{group_id}/location",
    response_model=GroupLocationResponse,
)
def update_group_location(
    group_id: str,
    request: GroupLocationUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return group_location_service.update_location(
        db=db,
        group_id=group_id,
        latitude=request.latitude,
        longitude=request.longitude,
        name=request.name,
    )


@router.delete(
    "/{group_id}/location",
)
def delete_group_location(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group_location_service.delete_location(
        db=db,
        group_id=group_id,
    )

    return {
        "message": "Group location deleted successfully"
    }