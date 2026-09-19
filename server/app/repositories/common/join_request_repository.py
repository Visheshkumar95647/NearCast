from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.common.join_request import JoinRequest
from app.models.user.user import User


class JoinRequestRepository:

    def get_by_id(
        self,
        db: Session,
        request_id: str,
    ) -> JoinRequest | None:

        return db.get(JoinRequest, request_id)

    def get_pending_request(
        self,
        db: Session,
        user_id: str,
        group_id: str,
    ) -> JoinRequest | None:

        result = db.execute(
            select(JoinRequest).where(
                JoinRequest.user_id == user_id,
                JoinRequest.group_id == group_id,
                JoinRequest.status == "pending",
            )
        )

        return result.scalar_one_or_none()

    def get_group_requests(
        self,
        db: Session,
        group_id: str,
    ) -> list[tuple[JoinRequest, User]]:

        result = db.execute(
            select(JoinRequest, User)
            .join(User, User.id == JoinRequest.user_id)
            .where(
                JoinRequest.group_id == group_id,
                JoinRequest.status == "pending",
            )
            .order_by(JoinRequest.requested_at.asc())
        )

        return list(result.all())

    def create(
        self,
        db: Session,
        join_request: JoinRequest,
    ) -> JoinRequest:

        db.add(join_request)
        db.commit()
        db.refresh(join_request)

        return join_request

    def update(
        self,
        db: Session,
        join_request: JoinRequest,
    ) -> JoinRequest:

        db.commit()
        db.refresh(join_request)

        return join_request

    def get_user_request(
        self,
        db: Session,
        user_id: str,
        group_id: str,
    ) -> JoinRequest | None:

        result = db.execute(
            select(JoinRequest)
            .where(
                JoinRequest.user_id == user_id,
                JoinRequest.group_id == group_id,
            )
            .order_by(JoinRequest.requested_at.desc())
        )

        return result.scalars().first()