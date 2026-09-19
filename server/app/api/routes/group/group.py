from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user.user import User
from app.schemas.group.group import (
    GroupCreateRequest,
    GroupResponse,
    GroupUpdateRequest,
)
from app.services.group.group_service import GroupService


router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
)

group_service = GroupService()


@router.post(
    "",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_group(
    data: GroupCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return group_service.create_group(
    db=db,
    user_id=str(current_user.id),
    name=data.name,
    description=data.description,
    is_private=data.is_private,
    )


@router.get(
    "",
    response_model=list[GroupResponse],
)
def get_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return group_service.get_groups(db)


@router.get(
    "/{group_id}",
    response_model=GroupResponse,
)
def get_group(
    group_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return group_service.get_group(
        db=db,
        group_id=group_id,
    )


@router.patch(
    "/{group_id}",
    response_model=GroupResponse,
)
def update_group(
    group_id: str,
    data: GroupUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return group_service.update_group(
        db=db,
        group_id=group_id,
        name=data.name,
        description=data.description,
        is_private=data.is_private,
        is_active=data.is_active,
    )


@router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_group(
    group_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group_service.delete_group(
        db=db,
        group_id=group_id,
    )