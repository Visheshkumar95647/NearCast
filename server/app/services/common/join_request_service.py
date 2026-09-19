from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.common.join_request import JoinRequest
from app.models.group.group_member import GroupMember
from app.models.user.user import User
from app.repositories.common.join_request_repository import JoinRequestRepository
from app.repositories.group.group_member_repository import GroupMemberRepository


class JoinRequestService:

    def __init__(self):
        self.join_request_repository = JoinRequestRepository()
        self.group_member_repository = GroupMemberRepository()

    def get_group_requests(
        self,
        db: Session,
        user_id: str,
        group_id: str,
    ) -> list[dict]:

        if not self.group_member_repository.is_admin(
            db,
            user_id,
            group_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only group admins can view join requests",
            )

        requests = self.join_request_repository.get_group_requests(
            db,
            group_id,
        )

        return [
            {
                "id": str(join_request.id),
                "user_id": str(join_request.user_id),
                "group_id": str(join_request.group_id),
                "username": user.username,
                "status": join_request.status,
                "requested_at": join_request.requested_at,
                "reviewed_at": join_request.reviewed_at,
            }
            for join_request, user in requests
        ]

    def get_user_request(
        self,
        db: Session,
        user_id: str,
        group_id: str,
    ) -> dict | None:

        join_request = self.join_request_repository.get_user_request(
            db,
            user_id,
            group_id,
        )

        if not join_request:
            return None

        user = db.get(User, join_request.user_id)

        return {
            "id": str(join_request.id),
            "user_id": str(join_request.user_id),
            "group_id": str(join_request.group_id),
            "username": user.username,
            "status": join_request.status,
            "requested_at": join_request.requested_at,
            "reviewed_at": join_request.reviewed_at,
        }

    def approve_request(
        self,
        db: Session,
        user_id: str,
        request_id: str,
    ) -> dict:

        join_request = self.join_request_repository.get_by_id(
            db,
            request_id,
        )

        if not join_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Join request not found",
            )

        group_id = str(join_request.group_id)

        if not self.group_member_repository.is_admin(
            db,
            user_id,
            group_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only group admins can approve join requests",
            )

        if join_request.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Join request has already been reviewed",
            )

        existing_member = self.group_member_repository.get_by_user_and_group(
            db,
            str(join_request.user_id),
            group_id,
        )

        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already a member of this group",
            )

        group_member = GroupMember(
            user_id=join_request.user_id,
            group_id=join_request.group_id,
            role="member",
            joined_at=datetime.now(timezone.utc),
        )

        db.add(group_member)

        join_request.status = "accepted"
        join_request.reviewed_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(join_request)

        user = db.get(User, join_request.user_id)

        return {
            "id": str(join_request.id),
            "user_id": str(join_request.user_id),
            "group_id": str(join_request.group_id),
            "username": user.username,
            "status": join_request.status,
            "requested_at": join_request.requested_at,
            "reviewed_at": join_request.reviewed_at,
        }

    def reject_request(
        self,
        db: Session,
        user_id: str,
        request_id: str,
    ) -> dict:

        join_request = self.join_request_repository.get_by_id(
            db,
            request_id,
        )

        if not join_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Join request not found",
            )

        group_id = str(join_request.group_id)

        if not self.group_member_repository.is_admin(
            db,
            user_id,
            group_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only group admins can reject join requests",
            )

        if join_request.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Join request has already been reviewed",
            )

        join_request.status = "rejected"
        join_request.reviewed_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(join_request)

        user = db.get(User, join_request.user_id)

        return {
            "id": str(join_request.id),
            "user_id": str(join_request.user_id),
            "group_id": str(join_request.group_id),
            "username": user.username,
            "status": join_request.status,
            "requested_at": join_request.requested_at,
            "reviewed_at": join_request.reviewed_at,
        }