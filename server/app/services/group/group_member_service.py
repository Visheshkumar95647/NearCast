from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.common.join_request import JoinRequest
from app.models.group.group import Group
from app.models.group.group_member import GroupMember
from app.repositories.common.join_request_repository import JoinRequestRepository
from app.repositories.group.group_member_repository import GroupMemberRepository


class GroupMemberService:

    def __init__(self):
        self.group_member_repository = GroupMemberRepository()
        self.join_request_repository = JoinRequestRepository()

    def join_group(
        self,
        db: Session,
        user_id: str,
        group_id: str,
    ) -> GroupMember | JoinRequest:

        group = db.get(Group, group_id)

        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found",
            )

        if not group.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Group is not active",
            )

        existing_member = self.group_member_repository.get_by_user_and_group(
            db,
            user_id,
            group_id,
        )

        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already a member of this group",
            )

        existing_request = self.join_request_repository.get_pending_request(
            db,
            user_id,
            group_id,
        )

        if existing_request:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Join request is already pending",
            )

        if group.is_private:
            join_request = JoinRequest(
                user_id=user_id,
                group_id=group_id,
                status="pending",
                requested_at=datetime.now(timezone.utc),
            )

            return self.join_request_repository.create(
                db,
                join_request,
            )

        group_member = GroupMember(
            user_id=user_id,
            group_id=group_id,
            role="member",
            joined_at=datetime.now(timezone.utc),
        )

        return self.group_member_repository.create(
            db,
            group_member,
        )

    def leave_group(
        self,
        db: Session,
        user_id: str,
        group_id: str,
    ) -> None:

        member = self.group_member_repository.get_by_user_and_group(
            db,
            user_id,
            group_id,
        )

        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not a member of this group",
            )

        group = db.get(Group, group_id)

        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found",
            )

        if member.role == "admin":

            admins = self.group_member_repository.get_admins_by_group_id(
                db,
                group_id,
            )

            db.delete(member)

            if len(admins) == 1:
                group.is_active = False

            db.commit()

            return

        self.group_member_repository.delete(
            db,
            member,
        )

    def promote_to_admin(
        self,
        db: Session,
        user_id: str,
        group_id: str,
        member_id: str,
    ) -> GroupMember:

        if not self.group_member_repository.is_admin(
            db,
            user_id,
            group_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only group admins can promote members",
            )

        member = db.get(GroupMember, member_id)

        if not member or str(member.group_id) != group_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group member not found",
            )

        if member.role == "admin":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already an admin",
            )

        member.role = "admin"

        db.commit()
        db.refresh(member)

        return member

    def demote_from_admin(
        self,
        db: Session,
        user_id: str,
        group_id: str,
        member_id: str,
    ) -> GroupMember:

        if not self.group_member_repository.is_admin(
            db,
            user_id,
            group_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only group admins can demote members",
            )

        member = db.get(GroupMember, member_id)

        if not member or str(member.group_id) != group_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group member not found",
            )

        if member.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not an admin",
            )

        if str(member.user_id) == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot demote yourself",
            )

        admins = self.group_member_repository.get_admins_by_group_id(
            db,
            group_id,
        )

        if len(admins) == 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot demote the last admin",
            )

        member.role = "member"

        db.commit()
        db.refresh(member)

        return member

    def get_members(
        self,
        db: Session,
        group_id: str,
    ) -> list[tuple[GroupMember, object]]:

        group = db.get(Group, group_id)

        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found",
            )

        return self.group_member_repository.get_members(
            db,
            group_id,
        )