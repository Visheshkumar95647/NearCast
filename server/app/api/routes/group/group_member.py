from typing import Union

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db

from app.models.user.user import User

from app.schemas.group.group_member import (
    GroupMemberResponse,
    JoinRequestResponse,
)

from app.services.group.group_member_service import GroupMemberService


router = APIRouter(
    prefix="/groups",
    tags=["Group Members"],
)

group_member_service = GroupMemberService()


@router.post(
    "/{group_id}/members",
    response_model=Union[GroupMemberResponse, JoinRequestResponse],
)
def join_group(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return group_member_service.join_group(
        db=db,
        user_id=str(current_user.id),
        group_id=group_id,
    )


@router.get(
    "/{group_id}/members",
    response_model=list[GroupMemberResponse],
)
def get_group_members(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    members = group_member_service.get_members(
        db=db,
        group_id=group_id,
    )

    return [
        {
            "id": str(member.id),
            "user_id": str(member.user_id),
            "group_id": str(member.group_id),
            "username": user.username,
            "role": member.role,
            "joined_at": member.joined_at,
        }
        for member, user in members
    ]


@router.delete(
    "/{group_id}/members/me",
)
def leave_group(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group_member_service.leave_group(
        db=db,
        user_id=str(current_user.id),
        group_id=group_id,
    )

    return {
        "message": "You have left the group successfully"
    }

@router.patch(
    "/{group_id}/members/{member_id}/admin",
    response_model=GroupMemberResponse,
)
def promote_member_to_admin(
    group_id: str,
    member_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    member = group_member_service.promote_to_admin(
        db=db,
        user_id=str(current_user.id),
        group_id=group_id,
        member_id=member_id,
    )

    return {
        "id": str(member.id),
        "user_id": str(member.user_id),
        "group_id": str(member.group_id),
        "username": db.get(User, member.user_id).username,
        "role": member.role,
        "joined_at": member.joined_at,
    }
@router.patch(
    "/{group_id}/members/{member_id}/demote",
    response_model=GroupMemberResponse,
)
def demote_member_from_admin(
    group_id: str,
    member_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    member = group_member_service.demote_from_admin(
        db=db,
        user_id=str(current_user.id),
        group_id=group_id,
        member_id=member_id,
    )

    return {
        "id": str(member.id),
        "user_id": str(member.user_id),
        "group_id": str(member.group_id),
        "username": db.get(User, member.user_id).username,
        "role": member.role,
        "joined_at": member.joined_at,
    }